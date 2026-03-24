//! Auto-generated uco-observable types for the CASE/UCO ontology.

use serde::Serialize;
use crate::graph::CaseObject;

use crate::uco::configuration::Configuration;
use crate::uco::core::UcoObject;
use crate::uco::identity::Identity;
use crate::uco::identity::Organization;
use crate::uco::location::Location;
use crate::uco::types::ControlledDictionary;
use crate::uco::types::Dictionary;
use crate::uco::types::Hash;
use crate::uco::types::Thread;

/// Vocabulary: WhoisDNSSECTypeVocab
#[derive(Debug, Clone, Serialize)]
pub struct WhoisDNSSECTypeVocab;

impl WhoisDNSSECTypeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WhoisDNSSECTypeVocab";
    pub const SIGNED: &'static str = "Signed";
    pub const UNSIGNED: &'static str = "Unsigned";
}

/// Vocabulary: WindowsVolumeAttributeVocab
#[derive(Debug, Clone, Serialize)]
pub struct WindowsVolumeAttributeVocab;

impl WindowsVolumeAttributeVocab {
    pub const IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/vocabulary/WindowsVolumeAttributeVocab";
    pub const HIDDEN: &'static str = "Hidden";
    pub const NODEFAULTDRIVELETTER: &'static str = "NoDefaultDriveLetter";
    pub const READONLY: &'static str = "ReadOnly";
    pub const SHADOWCOPY: &'static str = "ShadowCopy";
}

/// An API (application programming interface) is a computing interface that defines interactions between multiple software or mixed hardware-software intermediaries. It defines the kinds of calls or requ
#[derive(Debug, Clone, Serialize)]
pub struct API {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl API {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/API";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> APIBuilder {
        APIBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct APIBuilder {
}

impl APIBuilder {
    pub fn build(self) -> API {
        API {
            class_iri: API::CLASS_IRI,
        }
    }
}

impl CaseObject for API {
    fn class_iri() -> &'static str { API::CLASS_IRI }
    fn type_name() -> &'static str { "API" }
}

/// An ARP cache is a collection of Address Resolution Protocol (ARP) entries (mostly dynamic) that are created when an IP address is resolved to a MAC address (so the computer can effectively communicate
#[derive(Debug, Clone, Serialize)]
pub struct ARPCache {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ARPCache {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ARPCache";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ARPCacheBuilder {
        ARPCacheBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ARPCacheBuilder {
}

impl ARPCacheBuilder {
    pub fn build(self) -> ARPCache {
        ARPCache {
            class_iri: ARPCache::CLASS_IRI,
        }
    }
}

impl CaseObject for ARPCache {
    fn class_iri() -> &'static str { ARPCache::CLASS_IRI }
    fn type_name() -> &'static str { "ARPCache" }
}

/// An ARP cache entry is a single Address Resolution Protocol (ARP) response record that is created when an IP address is resolved to a MAC address (so the computer can effectively communicate with the I
#[derive(Debug, Clone, Serialize)]
pub struct ARPCacheEntry {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ARPCacheEntry {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ARPCacheEntry";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ARPCacheEntryBuilder {
        ARPCacheEntryBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ARPCacheEntryBuilder {
}

impl ARPCacheEntryBuilder {
    pub fn build(self) -> ARPCacheEntry {
        ARPCacheEntry {
            class_iri: ARPCacheEntry::CLASS_IRI,
        }
    }
}

impl CaseObject for ARPCacheEntry {
    fn class_iri() -> &'static str { ARPCacheEntry::CLASS_IRI }
    fn type_name() -> &'static str { "ARPCacheEntry" }
}

/// An account is an arrangement with an entity to enable and control the provision of some capability or service.
#[derive(Debug, Clone, Serialize)]
pub struct Account {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Account {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Account";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> AccountBuilder {
        AccountBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AccountBuilder {
}

impl AccountBuilder {
    pub fn build(self) -> Account {
        Account {
            class_iri: Account::CLASS_IRI,
        }
    }
}

impl CaseObject for Account {
    fn class_iri() -> &'static str { Account::CLASS_IRI }
    fn type_name() -> &'static str { "Account" }
}

/// An account authentication facet is a grouping of characteristics unique to the mechanism of accessing an account.
#[derive(Debug, Clone, Serialize)]
pub struct AccountAuthenticationFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:password")]
    pub password: Option<String>,
    #[serde(rename = "uco-observable:passwordLastChanged")]
    pub password_last_changed: Option<String>,
    #[serde(rename = "uco-observable:passwordType")]
    pub password_type: Option<String>,
}

impl AccountAuthenticationFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/AccountAuthenticationFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> AccountAuthenticationFacetBuilder {
        AccountAuthenticationFacetBuilder {
            password: None,
            password_last_changed: None,
            password_type: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AccountAuthenticationFacetBuilder {
    password: Option<String>,
    password_last_changed: Option<String>,
    password_type: Option<String>,
}

impl AccountAuthenticationFacetBuilder {
    pub fn password(mut self, value: String) -> Self {
        self.password = Some(value);
        self
    }

    pub fn password_last_changed(mut self, value: String) -> Self {
        self.password_last_changed = Some(value);
        self
    }

    pub fn password_type(mut self, value: String) -> Self {
        self.password_type = Some(value);
        self
    }

    pub fn build(self) -> AccountAuthenticationFacet {
        AccountAuthenticationFacet {
            class_iri: AccountAuthenticationFacet::CLASS_IRI,
            password: self.password,
            password_last_changed: self.password_last_changed,
            password_type: self.password_type,
        }
    }
}

impl CaseObject for AccountAuthenticationFacet {
    fn class_iri() -> &'static str { AccountAuthenticationFacet::CLASS_IRI }
    fn type_name() -> &'static str { "AccountAuthenticationFacet" }
}

/// An account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of some capability or service.
#[derive(Debug, Clone, Serialize)]
pub struct AccountFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:accountIdentifier")]
    pub account_identifier: Option<String>,
    #[serde(rename = "uco-observable:accountIssuer")]
    pub account_issuer: Option<UcoObject>,
    #[serde(rename = "uco-observable:accountType")]
    pub account_type: Vec<String>,
    #[serde(rename = "uco-observable:expirationTime")]
    pub expiration_time: Option<String>,
    #[serde(rename = "uco-observable:isActive")]
    pub is_active: Option<bool>,
    #[serde(rename = "uco-observable:modifiedTime")]
    pub modified_time: Option<String>,
    #[serde(rename = "uco-observable:observableCreatedTime")]
    pub observable_created_time: Option<String>,
    #[serde(rename = "uco-observable:owner")]
    pub owner: Option<UcoObject>,
}

impl AccountFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/AccountFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> AccountFacetBuilder {
        AccountFacetBuilder {
            account_identifier: None,
            account_issuer: None,
            account_type: Vec::new(),
            expiration_time: None,
            is_active: None,
            modified_time: None,
            observable_created_time: None,
            owner: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AccountFacetBuilder {
    account_identifier: Option<String>,
    account_issuer: Option<UcoObject>,
    account_type: Vec<String>,
    expiration_time: Option<String>,
    is_active: Option<bool>,
    modified_time: Option<String>,
    observable_created_time: Option<String>,
    owner: Option<UcoObject>,
}

impl AccountFacetBuilder {
    pub fn account_identifier(mut self, value: String) -> Self {
        self.account_identifier = Some(value);
        self
    }

    pub fn account_issuer(mut self, value: UcoObject) -> Self {
        self.account_issuer = Some(value);
        self
    }

    pub fn account_type(mut self, value: Vec<String>) -> Self {
        self.account_type = value;
        self
    }

    pub fn expiration_time(mut self, value: String) -> Self {
        self.expiration_time = Some(value);
        self
    }

    pub fn is_active(mut self, value: bool) -> Self {
        self.is_active = Some(value);
        self
    }

    pub fn modified_time(mut self, value: String) -> Self {
        self.modified_time = Some(value);
        self
    }

    pub fn observable_created_time(mut self, value: String) -> Self {
        self.observable_created_time = Some(value);
        self
    }

    pub fn owner(mut self, value: UcoObject) -> Self {
        self.owner = Some(value);
        self
    }

    pub fn build(self) -> AccountFacet {
        AccountFacet {
            class_iri: AccountFacet::CLASS_IRI,
            account_identifier: self.account_identifier,
            account_issuer: self.account_issuer,
            account_type: self.account_type,
            expiration_time: self.expiration_time,
            is_active: self.is_active,
            modified_time: self.modified_time,
            observable_created_time: self.observable_created_time,
            owner: self.owner,
        }
    }
}

impl CaseObject for AccountFacet {
    fn class_iri() -> &'static str { AccountFacet::CLASS_IRI }
    fn type_name() -> &'static str { "AccountFacet" }
}

/// An adaptor is a device that physically converts the pin outputs but does not alter the underlying protocol (e.g. uSD to SD, CF to ATA, etc.)
#[derive(Debug, Clone, Serialize)]
pub struct Adaptor {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Adaptor {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Adaptor";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> AdaptorBuilder {
        AdaptorBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AdaptorBuilder {
}

impl AdaptorBuilder {
    pub fn build(self) -> Adaptor {
        Adaptor {
            class_iri: Adaptor::CLASS_IRI,
        }
    }
}

impl CaseObject for Adaptor {
    fn class_iri() -> &'static str { Adaptor::CLASS_IRI }
    fn type_name() -> &'static str { "Adaptor" }
}

/// An address is an identifier assigned to enable routing and management of information.
#[derive(Debug, Clone, Serialize)]
pub struct Address {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Address {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Address";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> AddressBuilder {
        AddressBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AddressBuilder {
}

impl AddressBuilder {
    pub fn build(self) -> Address {
        Address {
            class_iri: Address::CLASS_IRI,
        }
    }
}

impl CaseObject for Address {
    fn class_iri() -> &'static str { Address::CLASS_IRI }
    fn type_name() -> &'static str { "Address" }
}

/// An alternate data stream is data content stored within an NTFS file that is independent of the standard content stream of the file and is hidden from access by default NTFS file viewing mechanisms.
#[derive(Debug, Clone, Serialize)]
pub struct AlternateDataStream {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl AlternateDataStream {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/AlternateDataStream";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> AlternateDataStreamBuilder {
        AlternateDataStreamBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AlternateDataStreamBuilder {
}

impl AlternateDataStreamBuilder {
    pub fn build(self) -> AlternateDataStream {
        AlternateDataStream {
            class_iri: AlternateDataStream::CLASS_IRI,
        }
    }
}

impl CaseObject for AlternateDataStream {
    fn class_iri() -> &'static str { AlternateDataStream::CLASS_IRI }
    fn type_name() -> &'static str { "AlternateDataStream" }
}

/// An alternate data stream facet is a grouping of characteristics unique to data content stored within an NTFS file that is independent of the standard content stream of the file and is hidden from acce
#[derive(Debug, Clone, Serialize)]
pub struct AlternateDataStreamFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:name")]
    pub name: Option<String>,
    #[serde(rename = "uco-observable:hashes")]
    pub hashes: Option<Hash>,
    #[serde(rename = "uco-observable:size")]
    pub size: Option<i64>,
}

impl AlternateDataStreamFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/AlternateDataStreamFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> AlternateDataStreamFacetBuilder {
        AlternateDataStreamFacetBuilder {
            name: None,
            hashes: None,
            size: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AlternateDataStreamFacetBuilder {
    name: Option<String>,
    hashes: Option<Hash>,
    size: Option<i64>,
}

impl AlternateDataStreamFacetBuilder {
    pub fn name(mut self, value: String) -> Self {
        self.name = Some(value);
        self
    }

    pub fn hashes(mut self, value: Hash) -> Self {
        self.hashes = Some(value);
        self
    }

    pub fn size(mut self, value: i64) -> Self {
        self.size = Some(value);
        self
    }

    pub fn build(self) -> AlternateDataStreamFacet {
        AlternateDataStreamFacet {
            class_iri: AlternateDataStreamFacet::CLASS_IRI,
            name: self.name,
            hashes: self.hashes,
            size: self.size,
        }
    }
}

impl CaseObject for AlternateDataStreamFacet {
    fn class_iri() -> &'static str { AlternateDataStreamFacet::CLASS_IRI }
    fn type_name() -> &'static str { "AlternateDataStreamFacet" }
}

/// An Android device is a device running the Android operating system. [based on https://en.wikipedia.org/wiki/Android_(operating_system)]
#[derive(Debug, Clone, Serialize)]
pub struct AndroidDevice {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl AndroidDevice {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/AndroidDevice";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> AndroidDeviceBuilder {
        AndroidDeviceBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AndroidDeviceBuilder {
}

impl AndroidDeviceBuilder {
    pub fn build(self) -> AndroidDevice {
        AndroidDevice {
            class_iri: AndroidDevice::CLASS_IRI,
        }
    }
}

impl CaseObject for AndroidDevice {
    fn class_iri() -> &'static str { AndroidDevice::CLASS_IRI }
    fn type_name() -> &'static str { "AndroidDevice" }
}

/// An Android device facet is a grouping of characteristics unique to an Android device. [based on https://en.wikipedia.org/wiki/Android_(operating_system)]
#[derive(Debug, Clone, Serialize)]
pub struct AndroidDeviceFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:androidFingerprint")]
    pub android_fingerprint: Option<String>,
    #[serde(rename = "uco-observable:androidID")]
    pub android_id: Option<Vec<u8>>,
    #[serde(rename = "uco-observable:androidVersion")]
    pub android_version: Option<String>,
    #[serde(rename = "uco-observable:isADBRootEnabled")]
    pub is_adb_root_enabled: Option<bool>,
    #[serde(rename = "uco-observable:isSURootEnabled")]
    pub is_su_root_enabled: Option<bool>,
}

impl AndroidDeviceFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/AndroidDeviceFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> AndroidDeviceFacetBuilder {
        AndroidDeviceFacetBuilder {
            android_fingerprint: None,
            android_id: None,
            android_version: None,
            is_adb_root_enabled: None,
            is_su_root_enabled: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AndroidDeviceFacetBuilder {
    android_fingerprint: Option<String>,
    android_id: Option<Vec<u8>>,
    android_version: Option<String>,
    is_adb_root_enabled: Option<bool>,
    is_su_root_enabled: Option<bool>,
}

impl AndroidDeviceFacetBuilder {
    pub fn android_fingerprint(mut self, value: String) -> Self {
        self.android_fingerprint = Some(value);
        self
    }

    pub fn android_id(mut self, value: Vec<u8>) -> Self {
        self.android_id = Some(value);
        self
    }

    pub fn android_version(mut self, value: String) -> Self {
        self.android_version = Some(value);
        self
    }

    pub fn is_adb_root_enabled(mut self, value: bool) -> Self {
        self.is_adb_root_enabled = Some(value);
        self
    }

    pub fn is_su_root_enabled(mut self, value: bool) -> Self {
        self.is_su_root_enabled = Some(value);
        self
    }

    pub fn build(self) -> AndroidDeviceFacet {
        AndroidDeviceFacet {
            class_iri: AndroidDeviceFacet::CLASS_IRI,
            android_fingerprint: self.android_fingerprint,
            android_id: self.android_id,
            android_version: self.android_version,
            is_adb_root_enabled: self.is_adb_root_enabled,
            is_su_root_enabled: self.is_su_root_enabled,
        }
    }
}

impl CaseObject for AndroidDeviceFacet {
    fn class_iri() -> &'static str { AndroidDeviceFacet::CLASS_IRI }
    fn type_name() -> &'static str { "AndroidDeviceFacet" }
}

/// An android phone is a smart phone that applies the Android mobile operating system.
#[derive(Debug, Clone, Serialize)]
pub struct AndroidPhone {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl AndroidPhone {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/AndroidPhone";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> AndroidPhoneBuilder {
        AndroidPhoneBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AndroidPhoneBuilder {
}

impl AndroidPhoneBuilder {
    pub fn build(self) -> AndroidPhone {
        AndroidPhone {
            class_iri: AndroidPhone::CLASS_IRI,
        }
    }
}

impl CaseObject for AndroidPhone {
    fn class_iri() -> &'static str { AndroidPhone::CLASS_IRI }
    fn type_name() -> &'static str { "AndroidPhone" }
}

/// An antenna alignment facet contains the metadata surrounding the cell tower's antenna position.
#[derive(Debug, Clone, Serialize)]
pub struct AntennaFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:antennaHeight")]
    pub antenna_height: Option<f64>,
    #[serde(rename = "uco-observable:azimuth")]
    pub azimuth: Option<f64>,
    #[serde(rename = "uco-observable:elevation")]
    pub elevation: Option<f64>,
    #[serde(rename = "uco-observable:horizontalBeamWidth")]
    pub horizontal_beam_width: Option<f64>,
    #[serde(rename = "uco-observable:signalStrength")]
    pub signal_strength: Option<f64>,
    #[serde(rename = "uco-observable:skew")]
    pub skew: Option<f64>,
}

impl AntennaFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/AntennaFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> AntennaFacetBuilder {
        AntennaFacetBuilder {
            antenna_height: None,
            azimuth: None,
            elevation: None,
            horizontal_beam_width: None,
            signal_strength: None,
            skew: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AntennaFacetBuilder {
    antenna_height: Option<f64>,
    azimuth: Option<f64>,
    elevation: Option<f64>,
    horizontal_beam_width: Option<f64>,
    signal_strength: Option<f64>,
    skew: Option<f64>,
}

impl AntennaFacetBuilder {
    pub fn antenna_height(mut self, value: f64) -> Self {
        self.antenna_height = Some(value);
        self
    }

    pub fn azimuth(mut self, value: f64) -> Self {
        self.azimuth = Some(value);
        self
    }

    pub fn elevation(mut self, value: f64) -> Self {
        self.elevation = Some(value);
        self
    }

    pub fn horizontal_beam_width(mut self, value: f64) -> Self {
        self.horizontal_beam_width = Some(value);
        self
    }

    pub fn signal_strength(mut self, value: f64) -> Self {
        self.signal_strength = Some(value);
        self
    }

    pub fn skew(mut self, value: f64) -> Self {
        self.skew = Some(value);
        self
    }

    pub fn build(self) -> AntennaFacet {
        AntennaFacet {
            class_iri: AntennaFacet::CLASS_IRI,
            antenna_height: self.antenna_height,
            azimuth: self.azimuth,
            elevation: self.elevation,
            horizontal_beam_width: self.horizontal_beam_width,
            signal_strength: self.signal_strength,
            skew: self.skew,
        }
    }
}

impl CaseObject for AntennaFacet {
    fn class_iri() -> &'static str { AntennaFacet::CLASS_IRI }
    fn type_name() -> &'static str { "AntennaFacet" }
}

/// An apple device is a smart device that applies either the MacOS or iOS operating system.
#[derive(Debug, Clone, Serialize)]
pub struct AppleDevice {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl AppleDevice {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/AppleDevice";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> AppleDeviceBuilder {
        AppleDeviceBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AppleDeviceBuilder {
}

impl AppleDeviceBuilder {
    pub fn build(self) -> AppleDevice {
        AppleDevice {
            class_iri: AppleDevice::CLASS_IRI,
        }
    }
}

impl CaseObject for AppleDevice {
    fn class_iri() -> &'static str { AppleDevice::CLASS_IRI }
    fn type_name() -> &'static str { "AppleDevice" }
}

/// An appliance is a purpose-built computer with software or firmware that is designed to provide a specific computing capability or resource. [based on https://en.wikipedia.org/wiki/Computer_appliance]
#[derive(Debug, Clone, Serialize)]
pub struct Appliance {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Appliance {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Appliance";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ApplianceBuilder {
        ApplianceBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ApplianceBuilder {
}

impl ApplianceBuilder {
    pub fn build(self) -> Appliance {
        Appliance {
            class_iri: Appliance::CLASS_IRI,
        }
    }
}

impl CaseObject for Appliance {
    fn class_iri() -> &'static str { Appliance::CLASS_IRI }
    fn type_name() -> &'static str { "Appliance" }
}

/// An application is a particular software program designed for end users.
#[derive(Debug, Clone, Serialize)]
pub struct Application {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Application {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Application";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ApplicationBuilder {
        ApplicationBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ApplicationBuilder {
}

impl ApplicationBuilder {
    pub fn build(self) -> Application {
        Application {
            class_iri: Application::CLASS_IRI,
        }
    }
}

impl CaseObject for Application {
    fn class_iri() -> &'static str { Application::CLASS_IRI }
    fn type_name() -> &'static str { "Application" }
}

/// An application account is an account within a particular software program designed for end users.
#[derive(Debug, Clone, Serialize)]
pub struct ApplicationAccount {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ApplicationAccount {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ApplicationAccount";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ApplicationAccountBuilder {
        ApplicationAccountBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ApplicationAccountBuilder {
}

impl ApplicationAccountBuilder {
    pub fn build(self) -> ApplicationAccount {
        ApplicationAccount {
            class_iri: ApplicationAccount::CLASS_IRI,
        }
    }
}

impl CaseObject for ApplicationAccount {
    fn class_iri() -> &'static str { ApplicationAccount::CLASS_IRI }
    fn type_name() -> &'static str { "ApplicationAccount" }
}

/// An application account facet is a grouping of characteristics unique to an account within a particular software program designed for end users.
#[derive(Debug, Clone, Serialize)]
pub struct ApplicationAccountFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:application")]
    pub application: Option<ObservableObject>,
}

impl ApplicationAccountFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ApplicationAccountFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ApplicationAccountFacetBuilder {
        ApplicationAccountFacetBuilder {
            application: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ApplicationAccountFacetBuilder {
    application: Option<ObservableObject>,
}

impl ApplicationAccountFacetBuilder {
    pub fn application(mut self, value: ObservableObject) -> Self {
        self.application = Some(value);
        self
    }

    pub fn build(self) -> ApplicationAccountFacet {
        ApplicationAccountFacet {
            class_iri: ApplicationAccountFacet::CLASS_IRI,
            application: self.application,
        }
    }
}

impl CaseObject for ApplicationAccountFacet {
    fn class_iri() -> &'static str { ApplicationAccountFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ApplicationAccountFacet" }
}

/// An application facet is a grouping of characteristics unique to a particular software program designed for end users.
#[derive(Debug, Clone, Serialize)]
pub struct ApplicationFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:applicationIdentifier")]
    pub application_identifier: Option<String>,
    #[serde(rename = "uco-observable:installedVersionHistory")]
    pub installed_version_history: Vec<ApplicationVersion>,
    #[serde(rename = "uco-observable:numberOfLaunches")]
    pub number_of_launches: Option<i64>,
    #[serde(rename = "uco-observable:operatingSystem")]
    pub operating_system: Option<ObservableObject>,
    #[serde(rename = "uco-observable:version")]
    pub version: Option<String>,
}

impl ApplicationFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ApplicationFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ApplicationFacetBuilder {
        ApplicationFacetBuilder {
            application_identifier: None,
            installed_version_history: Vec::new(),
            number_of_launches: None,
            operating_system: None,
            version: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ApplicationFacetBuilder {
    application_identifier: Option<String>,
    installed_version_history: Vec<ApplicationVersion>,
    number_of_launches: Option<i64>,
    operating_system: Option<ObservableObject>,
    version: Option<String>,
}

impl ApplicationFacetBuilder {
    pub fn application_identifier(mut self, value: String) -> Self {
        self.application_identifier = Some(value);
        self
    }

    pub fn installed_version_history(mut self, value: Vec<ApplicationVersion>) -> Self {
        self.installed_version_history = value;
        self
    }

    pub fn number_of_launches(mut self, value: i64) -> Self {
        self.number_of_launches = Some(value);
        self
    }

    pub fn operating_system(mut self, value: ObservableObject) -> Self {
        self.operating_system = Some(value);
        self
    }

    pub fn version(mut self, value: String) -> Self {
        self.version = Some(value);
        self
    }

    pub fn build(self) -> ApplicationFacet {
        ApplicationFacet {
            class_iri: ApplicationFacet::CLASS_IRI,
            application_identifier: self.application_identifier,
            installed_version_history: self.installed_version_history,
            number_of_launches: self.number_of_launches,
            operating_system: self.operating_system,
            version: self.version,
        }
    }
}

impl CaseObject for ApplicationFacet {
    fn class_iri() -> &'static str { ApplicationFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ApplicationFacet" }
}

/// An application version is a grouping of characteristics unique to a particular software program version.
#[derive(Debug, Clone, Serialize)]
pub struct ApplicationVersion {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:installDate")]
    pub install_date: Option<String>,
    #[serde(rename = "uco-observable:uninstallDate")]
    pub uninstall_date: Option<String>,
    #[serde(rename = "uco-observable:version")]
    pub version: Option<String>,
}

impl ApplicationVersion {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ApplicationVersion";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ApplicationVersionBuilder {
        ApplicationVersionBuilder {
            install_date: None,
            uninstall_date: None,
            version: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ApplicationVersionBuilder {
    install_date: Option<String>,
    uninstall_date: Option<String>,
    version: Option<String>,
}

impl ApplicationVersionBuilder {
    pub fn install_date(mut self, value: String) -> Self {
        self.install_date = Some(value);
        self
    }

    pub fn uninstall_date(mut self, value: String) -> Self {
        self.uninstall_date = Some(value);
        self
    }

    pub fn version(mut self, value: String) -> Self {
        self.version = Some(value);
        self
    }

    pub fn build(self) -> ApplicationVersion {
        ApplicationVersion {
            class_iri: ApplicationVersion::CLASS_IRI,
            install_date: self.install_date,
            uninstall_date: self.uninstall_date,
            version: self.version,
        }
    }
}

impl CaseObject for ApplicationVersion {
    fn class_iri() -> &'static str { ApplicationVersion::CLASS_IRI }
    fn type_name() -> &'static str { "ApplicationVersion" }
}

/// An archive file is a file that is composed of one or more computer files along with metadata.
#[derive(Debug, Clone, Serialize)]
pub struct ArchiveFile {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ArchiveFile {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ArchiveFile";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ArchiveFileBuilder {
        ArchiveFileBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ArchiveFileBuilder {
}

impl ArchiveFileBuilder {
    pub fn build(self) -> ArchiveFile {
        ArchiveFile {
            class_iri: ArchiveFile::CLASS_IRI,
        }
    }
}

impl CaseObject for ArchiveFile {
    fn class_iri() -> &'static str { ArchiveFile::CLASS_IRI }
    fn type_name() -> &'static str { "ArchiveFile" }
}

/// An archive file facet is a grouping of characteristics unique to a file that is composed of one or more computer files along with metadata.
#[derive(Debug, Clone, Serialize)]
pub struct ArchiveFileFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:archiveType")]
    pub archive_type: Option<String>,
    #[serde(rename = "uco-observable:comment")]
    pub comment: Option<String>,
    #[serde(rename = "uco-observable:version")]
    pub version: Option<String>,
}

impl ArchiveFileFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ArchiveFileFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ArchiveFileFacetBuilder {
        ArchiveFileFacetBuilder {
            archive_type: None,
            comment: None,
            version: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ArchiveFileFacetBuilder {
    archive_type: Option<String>,
    comment: Option<String>,
    version: Option<String>,
}

impl ArchiveFileFacetBuilder {
    pub fn archive_type(mut self, value: String) -> Self {
        self.archive_type = Some(value);
        self
    }

    pub fn comment(mut self, value: String) -> Self {
        self.comment = Some(value);
        self
    }

    pub fn version(mut self, value: String) -> Self {
        self.version = Some(value);
        self
    }

    pub fn build(self) -> ArchiveFileFacet {
        ArchiveFileFacet {
            class_iri: ArchiveFileFacet::CLASS_IRI,
            archive_type: self.archive_type,
            comment: self.comment,
            version: self.version,
        }
    }
}

impl CaseObject for ArchiveFileFacet {
    fn class_iri() -> &'static str { ArchiveFileFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ArchiveFileFacet" }
}

/// Audio is a digital representation of sound.
#[derive(Debug, Clone, Serialize)]
pub struct Audio {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Audio {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Audio";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> AudioBuilder {
        AudioBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AudioBuilder {
}

impl AudioBuilder {
    pub fn build(self) -> Audio {
        Audio {
            class_iri: Audio::CLASS_IRI,
        }
    }
}

impl CaseObject for Audio {
    fn class_iri() -> &'static str { Audio::CLASS_IRI }
    fn type_name() -> &'static str { "Audio" }
}

/// An audio facet is a grouping of characteristics unique to a digital representation of sound.
#[derive(Debug, Clone, Serialize)]
pub struct AudioFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:audioType")]
    pub audio_type: Option<String>,
    #[serde(rename = "uco-observable:bitRate")]
    pub bit_rate: Option<i64>,
    #[serde(rename = "uco-observable:duration")]
    pub duration: Option<i64>,
    #[serde(rename = "uco-observable:format")]
    pub format: Option<String>,
}

impl AudioFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/AudioFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> AudioFacetBuilder {
        AudioFacetBuilder {
            audio_type: None,
            bit_rate: None,
            duration: None,
            format: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AudioFacetBuilder {
    audio_type: Option<String>,
    bit_rate: Option<i64>,
    duration: Option<i64>,
    format: Option<String>,
}

impl AudioFacetBuilder {
    pub fn audio_type(mut self, value: String) -> Self {
        self.audio_type = Some(value);
        self
    }

    pub fn bit_rate(mut self, value: i64) -> Self {
        self.bit_rate = Some(value);
        self
    }

    pub fn duration(mut self, value: i64) -> Self {
        self.duration = Some(value);
        self
    }

    pub fn format(mut self, value: String) -> Self {
        self.format = Some(value);
        self
    }

    pub fn build(self) -> AudioFacet {
        AudioFacet {
            class_iri: AudioFacet::CLASS_IRI,
            audio_type: self.audio_type,
            bit_rate: self.bit_rate,
            duration: self.duration,
            format: self.format,
        }
    }
}

impl CaseObject for AudioFacet {
    fn class_iri() -> &'static str { AudioFacet::CLASS_IRI }
    fn type_name() -> &'static str { "AudioFacet" }
}

/// An autonomous system is a collection of connected Internet Protocol (IP) routing prefixes under the control of one or more network operators on behalf of a single administrative entity or domain that 
#[derive(Debug, Clone, Serialize)]
pub struct AutonomousSystem {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl AutonomousSystem {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/AutonomousSystem";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> AutonomousSystemBuilder {
        AutonomousSystemBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AutonomousSystemBuilder {
}

impl AutonomousSystemBuilder {
    pub fn build(self) -> AutonomousSystem {
        AutonomousSystem {
            class_iri: AutonomousSystem::CLASS_IRI,
        }
    }
}

impl CaseObject for AutonomousSystem {
    fn class_iri() -> &'static str { AutonomousSystem::CLASS_IRI }
    fn type_name() -> &'static str { "AutonomousSystem" }
}

/// An autonomous system facet is a grouping of characteristics unique to a collection of connected Internet Protocol (IP) routing prefixes under the control of one or more network operators on behalf of 
#[derive(Debug, Clone, Serialize)]
pub struct AutonomousSystemFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:asHandle")]
    pub as_handle: Option<String>,
    #[serde(rename = "uco-observable:number")]
    pub number: Option<i64>,
    #[serde(rename = "uco-observable:regionalInternetRegistry")]
    pub regional_internet_registry: Vec<String>,
}

impl AutonomousSystemFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/AutonomousSystemFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> AutonomousSystemFacetBuilder {
        AutonomousSystemFacetBuilder {
            as_handle: None,
            number: None,
            regional_internet_registry: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct AutonomousSystemFacetBuilder {
    as_handle: Option<String>,
    number: Option<i64>,
    regional_internet_registry: Vec<String>,
}

impl AutonomousSystemFacetBuilder {
    pub fn as_handle(mut self, value: String) -> Self {
        self.as_handle = Some(value);
        self
    }

    pub fn number(mut self, value: i64) -> Self {
        self.number = Some(value);
        self
    }

    pub fn regional_internet_registry(mut self, value: Vec<String>) -> Self {
        self.regional_internet_registry = value;
        self
    }

    pub fn build(self) -> AutonomousSystemFacet {
        AutonomousSystemFacet {
            class_iri: AutonomousSystemFacet::CLASS_IRI,
            as_handle: self.as_handle,
            number: self.number,
            regional_internet_registry: self.regional_internet_registry,
        }
    }
}

impl CaseObject for AutonomousSystemFacet {
    fn class_iri() -> &'static str { AutonomousSystemFacet::CLASS_IRI }
    fn type_name() -> &'static str { "AutonomousSystemFacet" }
}

/// A blackberry phone is a smart phone that applies the Blackberry OS mobile operating system. (Blackberry 10 re-introduces Blackberry OS, prior to that the OS was Android.)
#[derive(Debug, Clone, Serialize)]
pub struct BlackberryPhone {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl BlackberryPhone {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/BlackberryPhone";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> BlackberryPhoneBuilder {
        BlackberryPhoneBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct BlackberryPhoneBuilder {
}

impl BlackberryPhoneBuilder {
    pub fn build(self) -> BlackberryPhone {
        BlackberryPhone {
            class_iri: BlackberryPhone::CLASS_IRI,
        }
    }
}

impl CaseObject for BlackberryPhone {
    fn class_iri() -> &'static str { BlackberryPhone::CLASS_IRI }
    fn type_name() -> &'static str { "BlackberryPhone" }
}

/// A block device node is a UNIX filesystem special file that serves as a conduit to communicate with devices, providing buffered randomly accesible input and output. Block device nodes are used to apply
#[derive(Debug, Clone, Serialize)]
pub struct BlockDeviceNode {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl BlockDeviceNode {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/BlockDeviceNode";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> BlockDeviceNodeBuilder {
        BlockDeviceNodeBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct BlockDeviceNodeBuilder {
}

impl BlockDeviceNodeBuilder {
    pub fn build(self) -> BlockDeviceNode {
        BlockDeviceNode {
            class_iri: BlockDeviceNode::CLASS_IRI,
        }
    }
}

impl CaseObject for BlockDeviceNode {
    fn class_iri() -> &'static str { BlockDeviceNode::CLASS_IRI }
    fn type_name() -> &'static str { "BlockDeviceNode" }
}

/// A Bluetooth address is a Bluetooth standard conformant identifier assigned to a Bluetooth device to enable routing and management of Bluetooth standards conformant communication to or from that device
#[derive(Debug, Clone, Serialize)]
pub struct BluetoothAddress {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl BluetoothAddress {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/BluetoothAddress";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> BluetoothAddressBuilder {
        BluetoothAddressBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct BluetoothAddressBuilder {
}

impl BluetoothAddressBuilder {
    pub fn build(self) -> BluetoothAddress {
        BluetoothAddress {
            class_iri: BluetoothAddress::CLASS_IRI,
        }
    }
}

impl CaseObject for BluetoothAddress {
    fn class_iri() -> &'static str { BluetoothAddress::CLASS_IRI }
    fn type_name() -> &'static str { "BluetoothAddress" }
}

/// A Bluetooth address facet is a grouping of characteristics unique to a Bluetooth standard conformant identifier assigned to a Bluetooth device to enable routing and management of Bluetooth standards c
#[derive(Debug, Clone, Serialize)]
pub struct BluetoothAddressFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl BluetoothAddressFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/BluetoothAddressFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> BluetoothAddressFacetBuilder {
        BluetoothAddressFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct BluetoothAddressFacetBuilder {
}

impl BluetoothAddressFacetBuilder {
    pub fn build(self) -> BluetoothAddressFacet {
        BluetoothAddressFacet {
            class_iri: BluetoothAddressFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for BluetoothAddressFacet {
    fn class_iri() -> &'static str { BluetoothAddressFacet::CLASS_IRI }
    fn type_name() -> &'static str { "BluetoothAddressFacet" }
}

/// A bot configuration is a set of contextual settings for a software application that runs automated tasks (scripts) over the Internet at a much higher rate than would be possible for a human alone.
#[derive(Debug, Clone, Serialize)]
pub struct BotConfiguration {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl BotConfiguration {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/BotConfiguration";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> BotConfigurationBuilder {
        BotConfigurationBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct BotConfigurationBuilder {
}

impl BotConfigurationBuilder {
    pub fn build(self) -> BotConfiguration {
        BotConfiguration {
            class_iri: BotConfiguration::CLASS_IRI,
        }
    }
}

impl CaseObject for BotConfiguration {
    fn class_iri() -> &'static str { BotConfiguration::CLASS_IRI }
    fn type_name() -> &'static str { "BotConfiguration" }
}

/// A browser bookmark is a saved shortcut that directs a WWW (World Wide Web) browser software program to a particular WWW accessible resource. [based on https://techterms.com/definition/bookmark]
#[derive(Debug, Clone, Serialize)]
pub struct BrowserBookmark {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl BrowserBookmark {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/BrowserBookmark";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> BrowserBookmarkBuilder {
        BrowserBookmarkBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct BrowserBookmarkBuilder {
}

impl BrowserBookmarkBuilder {
    pub fn build(self) -> BrowserBookmark {
        BrowserBookmark {
            class_iri: BrowserBookmark::CLASS_IRI,
        }
    }
}

impl CaseObject for BrowserBookmark {
    fn class_iri() -> &'static str { BrowserBookmark::CLASS_IRI }
    fn type_name() -> &'static str { "BrowserBookmark" }
}

/// A browser bookmark facet is a grouping of characteristics unique to a saved shortcut that directs a WWW (World Wide Web) browser software program to a particular WWW accessible resource. [based on htt
#[derive(Debug, Clone, Serialize)]
pub struct BrowserBookmarkFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:accessedTime")]
    pub accessed_time: Option<String>,
    #[serde(rename = "uco-observable:application")]
    pub application: Option<ObservableObject>,
    #[serde(rename = "uco-observable:bookmarkPath")]
    pub bookmark_path: Option<String>,
    #[serde(rename = "uco-observable:modifiedTime")]
    pub modified_time: Option<String>,
    #[serde(rename = "uco-observable:observableCreatedTime")]
    pub observable_created_time: Option<String>,
    #[serde(rename = "uco-observable:urlTargeted")]
    pub url_targeted: Vec<String>,
    #[serde(rename = "uco-observable:visitCount")]
    pub visit_count: Option<i64>,
}

impl BrowserBookmarkFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/BrowserBookmarkFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> BrowserBookmarkFacetBuilder {
        BrowserBookmarkFacetBuilder {
            accessed_time: None,
            application: None,
            bookmark_path: None,
            modified_time: None,
            observable_created_time: None,
            url_targeted: Vec::new(),
            visit_count: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct BrowserBookmarkFacetBuilder {
    accessed_time: Option<String>,
    application: Option<ObservableObject>,
    bookmark_path: Option<String>,
    modified_time: Option<String>,
    observable_created_time: Option<String>,
    url_targeted: Vec<String>,
    visit_count: Option<i64>,
}

impl BrowserBookmarkFacetBuilder {
    pub fn accessed_time(mut self, value: String) -> Self {
        self.accessed_time = Some(value);
        self
    }

    pub fn application(mut self, value: ObservableObject) -> Self {
        self.application = Some(value);
        self
    }

    pub fn bookmark_path(mut self, value: String) -> Self {
        self.bookmark_path = Some(value);
        self
    }

    pub fn modified_time(mut self, value: String) -> Self {
        self.modified_time = Some(value);
        self
    }

    pub fn observable_created_time(mut self, value: String) -> Self {
        self.observable_created_time = Some(value);
        self
    }

    pub fn url_targeted(mut self, value: Vec<String>) -> Self {
        self.url_targeted = value;
        self
    }

    pub fn visit_count(mut self, value: i64) -> Self {
        self.visit_count = Some(value);
        self
    }

    pub fn build(self) -> BrowserBookmarkFacet {
        BrowserBookmarkFacet {
            class_iri: BrowserBookmarkFacet::CLASS_IRI,
            accessed_time: self.accessed_time,
            application: self.application,
            bookmark_path: self.bookmark_path,
            modified_time: self.modified_time,
            observable_created_time: self.observable_created_time,
            url_targeted: self.url_targeted,
            visit_count: self.visit_count,
        }
    }
}

impl CaseObject for BrowserBookmarkFacet {
    fn class_iri() -> &'static str { BrowserBookmarkFacet::CLASS_IRI }
    fn type_name() -> &'static str { "BrowserBookmarkFacet" }
}

/// A browser cookie is a piece of of data sent from a website and stored on the user's computer by the user's web browser while the user is browsing. [based on https://en.wikipedia.org/wiki/HTTP_cookie]
#[derive(Debug, Clone, Serialize)]
pub struct BrowserCookie {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl BrowserCookie {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/BrowserCookie";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> BrowserCookieBuilder {
        BrowserCookieBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct BrowserCookieBuilder {
}

impl BrowserCookieBuilder {
    pub fn build(self) -> BrowserCookie {
        BrowserCookie {
            class_iri: BrowserCookie::CLASS_IRI,
        }
    }
}

impl CaseObject for BrowserCookie {
    fn class_iri() -> &'static str { BrowserCookie::CLASS_IRI }
    fn type_name() -> &'static str { "BrowserCookie" }
}

/// A browser cookie facet is a grouping of characteristics unique to a piece of data sent from a website and stored on the user's computer by the user's web browser while the user is browsing. [based on 
#[derive(Debug, Clone, Serialize)]
pub struct BrowserCookieFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:accessedTime")]
    pub accessed_time: Option<String>,
    #[serde(rename = "uco-observable:application")]
    pub application: Option<ObservableObject>,
    #[serde(rename = "uco-observable:cookieDomain")]
    pub cookie_domain: Option<ObservableObject>,
    #[serde(rename = "uco-observable:cookieName")]
    pub cookie_name: Option<String>,
    #[serde(rename = "uco-observable:cookiePath")]
    pub cookie_path: Option<String>,
    #[serde(rename = "uco-observable:expirationTime")]
    pub expiration_time: Option<String>,
    #[serde(rename = "uco-observable:isSecure")]
    pub is_secure: Option<bool>,
    #[serde(rename = "uco-observable:observableCreatedTime")]
    pub observable_created_time: Option<String>,
}

impl BrowserCookieFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/BrowserCookieFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> BrowserCookieFacetBuilder {
        BrowserCookieFacetBuilder {
            accessed_time: None,
            application: None,
            cookie_domain: None,
            cookie_name: None,
            cookie_path: None,
            expiration_time: None,
            is_secure: None,
            observable_created_time: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct BrowserCookieFacetBuilder {
    accessed_time: Option<String>,
    application: Option<ObservableObject>,
    cookie_domain: Option<ObservableObject>,
    cookie_name: Option<String>,
    cookie_path: Option<String>,
    expiration_time: Option<String>,
    is_secure: Option<bool>,
    observable_created_time: Option<String>,
}

impl BrowserCookieFacetBuilder {
    pub fn accessed_time(mut self, value: String) -> Self {
        self.accessed_time = Some(value);
        self
    }

    pub fn application(mut self, value: ObservableObject) -> Self {
        self.application = Some(value);
        self
    }

    pub fn cookie_domain(mut self, value: ObservableObject) -> Self {
        self.cookie_domain = Some(value);
        self
    }

    pub fn cookie_name(mut self, value: String) -> Self {
        self.cookie_name = Some(value);
        self
    }

    pub fn cookie_path(mut self, value: String) -> Self {
        self.cookie_path = Some(value);
        self
    }

    pub fn expiration_time(mut self, value: String) -> Self {
        self.expiration_time = Some(value);
        self
    }

    pub fn is_secure(mut self, value: bool) -> Self {
        self.is_secure = Some(value);
        self
    }

    pub fn observable_created_time(mut self, value: String) -> Self {
        self.observable_created_time = Some(value);
        self
    }

    pub fn build(self) -> BrowserCookieFacet {
        BrowserCookieFacet {
            class_iri: BrowserCookieFacet::CLASS_IRI,
            accessed_time: self.accessed_time,
            application: self.application,
            cookie_domain: self.cookie_domain,
            cookie_name: self.cookie_name,
            cookie_path: self.cookie_path,
            expiration_time: self.expiration_time,
            is_secure: self.is_secure,
            observable_created_time: self.observable_created_time,
        }
    }
}

impl CaseObject for BrowserCookieFacet {
    fn class_iri() -> &'static str { BrowserCookieFacet::CLASS_IRI }
    fn type_name() -> &'static str { "BrowserCookieFacet" }
}

/// A calendar is a collection of appointments, meetings, and events.
#[derive(Debug, Clone, Serialize)]
pub struct Calendar {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Calendar {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Calendar";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> CalendarBuilder {
        CalendarBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CalendarBuilder {
}

impl CalendarBuilder {
    pub fn build(self) -> Calendar {
        Calendar {
            class_iri: Calendar::CLASS_IRI,
        }
    }
}

impl CaseObject for Calendar {
    fn class_iri() -> &'static str { Calendar::CLASS_IRI }
    fn type_name() -> &'static str { "Calendar" }
}

/// A calendar entry is an appointment, meeting or event within a collection of appointments, meetings and events.
#[derive(Debug, Clone, Serialize)]
pub struct CalendarEntry {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl CalendarEntry {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/CalendarEntry";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> CalendarEntryBuilder {
        CalendarEntryBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CalendarEntryBuilder {
}

impl CalendarEntryBuilder {
    pub fn build(self) -> CalendarEntry {
        CalendarEntry {
            class_iri: CalendarEntry::CLASS_IRI,
        }
    }
}

impl CaseObject for CalendarEntry {
    fn class_iri() -> &'static str { CalendarEntry::CLASS_IRI }
    fn type_name() -> &'static str { "CalendarEntry" }
}

/// A calendar entry facet is a grouping of characteristics unique to an appointment, meeting, or event within a collection of appointments, meetings, and events.
#[derive(Debug, Clone, Serialize)]
pub struct CalendarEntryFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:application")]
    pub application: Option<ObservableObject>,
    #[serde(rename = "uco-observable:attendant")]
    pub attendant: Vec<Identity>,
    #[serde(rename = "uco-observable:duration")]
    pub duration: Option<i64>,
    #[serde(rename = "uco-observable:endTime")]
    pub end_time: Option<String>,
    #[serde(rename = "uco-observable:eventStatus")]
    pub event_status: Option<String>,
    #[serde(rename = "uco-observable:eventType")]
    pub event_type: Option<String>,
    #[serde(rename = "uco-observable:isPrivate")]
    pub is_private: Option<bool>,
    #[serde(rename = "uco-observable:location")]
    pub location: Option<Location>,
    #[serde(rename = "uco-observable:modifiedTime")]
    pub modified_time: Option<String>,
    #[serde(rename = "uco-observable:observableCreatedTime")]
    pub observable_created_time: Option<String>,
    #[serde(rename = "uco-observable:owner")]
    pub owner: Option<UcoObject>,
    #[serde(rename = "uco-observable:recurrence")]
    pub recurrence: Option<String>,
    #[serde(rename = "uco-observable:remindTime")]
    pub remind_time: Option<String>,
    #[serde(rename = "uco-observable:startTime")]
    pub start_time: Option<String>,
    #[serde(rename = "uco-observable:subject")]
    pub subject: Option<String>,
}

impl CalendarEntryFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/CalendarEntryFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> CalendarEntryFacetBuilder {
        CalendarEntryFacetBuilder {
            application: None,
            attendant: Vec::new(),
            duration: None,
            end_time: None,
            event_status: None,
            event_type: None,
            is_private: None,
            location: None,
            modified_time: None,
            observable_created_time: None,
            owner: None,
            recurrence: None,
            remind_time: None,
            start_time: None,
            subject: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CalendarEntryFacetBuilder {
    application: Option<ObservableObject>,
    attendant: Vec<Identity>,
    duration: Option<i64>,
    end_time: Option<String>,
    event_status: Option<String>,
    event_type: Option<String>,
    is_private: Option<bool>,
    location: Option<Location>,
    modified_time: Option<String>,
    observable_created_time: Option<String>,
    owner: Option<UcoObject>,
    recurrence: Option<String>,
    remind_time: Option<String>,
    start_time: Option<String>,
    subject: Option<String>,
}

impl CalendarEntryFacetBuilder {
    pub fn application(mut self, value: ObservableObject) -> Self {
        self.application = Some(value);
        self
    }

    pub fn attendant(mut self, value: Vec<Identity>) -> Self {
        self.attendant = value;
        self
    }

    pub fn duration(mut self, value: i64) -> Self {
        self.duration = Some(value);
        self
    }

    pub fn end_time(mut self, value: String) -> Self {
        self.end_time = Some(value);
        self
    }

    pub fn event_status(mut self, value: String) -> Self {
        self.event_status = Some(value);
        self
    }

    pub fn event_type(mut self, value: String) -> Self {
        self.event_type = Some(value);
        self
    }

    pub fn is_private(mut self, value: bool) -> Self {
        self.is_private = Some(value);
        self
    }

    pub fn location(mut self, value: Location) -> Self {
        self.location = Some(value);
        self
    }

    pub fn modified_time(mut self, value: String) -> Self {
        self.modified_time = Some(value);
        self
    }

    pub fn observable_created_time(mut self, value: String) -> Self {
        self.observable_created_time = Some(value);
        self
    }

    pub fn owner(mut self, value: UcoObject) -> Self {
        self.owner = Some(value);
        self
    }

    pub fn recurrence(mut self, value: String) -> Self {
        self.recurrence = Some(value);
        self
    }

    pub fn remind_time(mut self, value: String) -> Self {
        self.remind_time = Some(value);
        self
    }

    pub fn start_time(mut self, value: String) -> Self {
        self.start_time = Some(value);
        self
    }

    pub fn subject(mut self, value: String) -> Self {
        self.subject = Some(value);
        self
    }

    pub fn build(self) -> CalendarEntryFacet {
        CalendarEntryFacet {
            class_iri: CalendarEntryFacet::CLASS_IRI,
            application: self.application,
            attendant: self.attendant,
            duration: self.duration,
            end_time: self.end_time,
            event_status: self.event_status,
            event_type: self.event_type,
            is_private: self.is_private,
            location: self.location,
            modified_time: self.modified_time,
            observable_created_time: self.observable_created_time,
            owner: self.owner,
            recurrence: self.recurrence,
            remind_time: self.remind_time,
            start_time: self.start_time,
            subject: self.subject,
        }
    }
}

impl CaseObject for CalendarEntryFacet {
    fn class_iri() -> &'static str { CalendarEntryFacet::CLASS_IRI }
    fn type_name() -> &'static str { "CalendarEntryFacet" }
}

/// A calendar facet is a grouping of characteristics unique to a collection of appointments, meetings, and events.
#[derive(Debug, Clone, Serialize)]
pub struct CalendarFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:application")]
    pub application: Option<ObservableObject>,
    #[serde(rename = "uco-observable:owner")]
    pub owner: Option<UcoObject>,
}

impl CalendarFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/CalendarFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> CalendarFacetBuilder {
        CalendarFacetBuilder {
            application: None,
            owner: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CalendarFacetBuilder {
    application: Option<ObservableObject>,
    owner: Option<UcoObject>,
}

impl CalendarFacetBuilder {
    pub fn application(mut self, value: ObservableObject) -> Self {
        self.application = Some(value);
        self
    }

    pub fn owner(mut self, value: UcoObject) -> Self {
        self.owner = Some(value);
        self
    }

    pub fn build(self) -> CalendarFacet {
        CalendarFacet {
            class_iri: CalendarFacet::CLASS_IRI,
            application: self.application,
            owner: self.owner,
        }
    }
}

impl CaseObject for CalendarFacet {
    fn class_iri() -> &'static str { CalendarFacet::CLASS_IRI }
    fn type_name() -> &'static str { "CalendarFacet" }
}

/// A call is a connection as part of a realtime cyber communication between one or more parties.
#[derive(Debug, Clone, Serialize)]
pub struct Call {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Call {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Call";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> CallBuilder {
        CallBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CallBuilder {
}

impl CallBuilder {
    pub fn build(self) -> Call {
        Call {
            class_iri: Call::CLASS_IRI,
        }
    }
}

impl CaseObject for Call {
    fn class_iri() -> &'static str { Call::CLASS_IRI }
    fn type_name() -> &'static str { "Call" }
}

/// A call facet is a grouping of characteristics unique to a connection as part of a realtime cyber communication between one or more parties.
#[derive(Debug, Clone, Serialize)]
pub struct CallFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:application")]
    pub application: Option<ObservableObject>,
    #[serde(rename = "uco-observable:callType")]
    pub call_type: Option<String>,
    #[serde(rename = "uco-observable:duration")]
    pub duration: Option<i64>,
    #[serde(rename = "uco-observable:endTime")]
    pub end_time: Option<String>,
    #[serde(rename = "uco-observable:from")]
    pub from: Option<ObservableObject>,
    #[serde(rename = "uco-observable:participant")]
    pub participant: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:startTime")]
    pub start_time: Option<String>,
    #[serde(rename = "uco-observable:to")]
    pub to: Vec<ObservableObject>,
}

impl CallFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/CallFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> CallFacetBuilder {
        CallFacetBuilder {
            application: None,
            call_type: None,
            duration: None,
            end_time: None,
            from: None,
            participant: Vec::new(),
            start_time: None,
            to: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CallFacetBuilder {
    application: Option<ObservableObject>,
    call_type: Option<String>,
    duration: Option<i64>,
    end_time: Option<String>,
    from: Option<ObservableObject>,
    participant: Vec<ObservableObject>,
    start_time: Option<String>,
    to: Vec<ObservableObject>,
}

impl CallFacetBuilder {
    pub fn application(mut self, value: ObservableObject) -> Self {
        self.application = Some(value);
        self
    }

    pub fn call_type(mut self, value: String) -> Self {
        self.call_type = Some(value);
        self
    }

    pub fn duration(mut self, value: i64) -> Self {
        self.duration = Some(value);
        self
    }

    pub fn end_time(mut self, value: String) -> Self {
        self.end_time = Some(value);
        self
    }

    pub fn from(mut self, value: ObservableObject) -> Self {
        self.from = Some(value);
        self
    }

    pub fn participant(mut self, value: Vec<ObservableObject>) -> Self {
        self.participant = value;
        self
    }

    pub fn start_time(mut self, value: String) -> Self {
        self.start_time = Some(value);
        self
    }

    pub fn to(mut self, value: Vec<ObservableObject>) -> Self {
        self.to = value;
        self
    }

    pub fn build(self) -> CallFacet {
        CallFacet {
            class_iri: CallFacet::CLASS_IRI,
            application: self.application,
            call_type: self.call_type,
            duration: self.duration,
            end_time: self.end_time,
            from: self.from,
            participant: self.participant,
            start_time: self.start_time,
            to: self.to,
        }
    }
}

impl CaseObject for CallFacet {
    fn class_iri() -> &'static str { CallFacet::CLASS_IRI }
    fn type_name() -> &'static str { "CallFacet" }
}

/// CapturedTelecommunicationsInformation
#[derive(Debug, Clone, Serialize)]
pub struct CapturedTelecommunicationsInformation {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl CapturedTelecommunicationsInformation {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/CapturedTelecommunicationsInformation";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> CapturedTelecommunicationsInformationBuilder {
        CapturedTelecommunicationsInformationBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CapturedTelecommunicationsInformationBuilder {
}

impl CapturedTelecommunicationsInformationBuilder {
    pub fn build(self) -> CapturedTelecommunicationsInformation {
        CapturedTelecommunicationsInformation {
            class_iri: CapturedTelecommunicationsInformation::CLASS_IRI,
        }
    }
}

impl CaseObject for CapturedTelecommunicationsInformation {
    fn class_iri() -> &'static str { CapturedTelecommunicationsInformation::CLASS_IRI }
    fn type_name() -> &'static str { "CapturedTelecommunicationsInformation" }
}

/// A captured telecommunications information facet represents certain information within captured or intercepted telecommunications data.
#[derive(Debug, Clone, Serialize)]
pub struct CapturedTelecommunicationsInformationFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:captureCellSite")]
    pub capture_cell_site: CellSite,
    #[serde(rename = "uco-observable:endTime")]
    pub end_time: Option<String>,
    #[serde(rename = "uco-observable:interceptedCallState")]
    pub intercepted_call_state: Option<String>,
    #[serde(rename = "uco-observable:startTime")]
    pub start_time: Option<String>,
}

impl CapturedTelecommunicationsInformationFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/CapturedTelecommunicationsInformationFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> CapturedTelecommunicationsInformationFacetBuilder {
        CapturedTelecommunicationsInformationFacetBuilder {
            capture_cell_site: None,
            end_time: None,
            intercepted_call_state: None,
            start_time: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CapturedTelecommunicationsInformationFacetBuilder {
    capture_cell_site: Option<CellSite>,
    end_time: Option<String>,
    intercepted_call_state: Option<String>,
    start_time: Option<String>,
}

impl CapturedTelecommunicationsInformationFacetBuilder {
    pub fn capture_cell_site(mut self, value: CellSite) -> Self {
        self.capture_cell_site = Some(value);
        self
    }

    pub fn end_time(mut self, value: String) -> Self {
        self.end_time = Some(value);
        self
    }

    pub fn intercepted_call_state(mut self, value: String) -> Self {
        self.intercepted_call_state = Some(value);
        self
    }

    pub fn start_time(mut self, value: String) -> Self {
        self.start_time = Some(value);
        self
    }

    pub fn build(self) -> CapturedTelecommunicationsInformationFacet {
        CapturedTelecommunicationsInformationFacet {
            class_iri: CapturedTelecommunicationsInformationFacet::CLASS_IRI,
            capture_cell_site: self.capture_cell_site.expect("missing required field: capture_cell_site"),
            end_time: self.end_time,
            intercepted_call_state: self.intercepted_call_state,
            start_time: self.start_time,
        }
    }
}

impl CaseObject for CapturedTelecommunicationsInformationFacet {
    fn class_iri() -> &'static str { CapturedTelecommunicationsInformationFacet::CLASS_IRI }
    fn type_name() -> &'static str { "CapturedTelecommunicationsInformationFacet" }
}

/// CellSite
#[derive(Debug, Clone, Serialize)]
pub struct CellSite {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl CellSite {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/CellSite";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> CellSiteBuilder {
        CellSiteBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CellSiteBuilder {
}

impl CellSiteBuilder {
    pub fn build(self) -> CellSite {
        CellSite {
            class_iri: CellSite::CLASS_IRI,
        }
    }
}

impl CaseObject for CellSite {
    fn class_iri() -> &'static str { CellSite::CLASS_IRI }
    fn type_name() -> &'static str { "CellSite" }
}

/// A cell site facet contains the metadata surrounding the cell site.
#[derive(Debug, Clone, Serialize)]
pub struct CellSiteFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:cellSiteCountryCode")]
    pub cell_site_country_code: Option<String>,
    #[serde(rename = "uco-observable:cellSiteIdentifier")]
    pub cell_site_identifier: Option<String>,
    #[serde(rename = "uco-observable:cellSiteLocationAreaCode")]
    pub cell_site_location_area_code: Option<String>,
    #[serde(rename = "uco-observable:cellSiteNetworkCode")]
    pub cell_site_network_code: Option<String>,
    #[serde(rename = "uco-observable:cellSiteType")]
    pub cell_site_type: Option<String>,
}

impl CellSiteFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/CellSiteFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> CellSiteFacetBuilder {
        CellSiteFacetBuilder {
            cell_site_country_code: None,
            cell_site_identifier: None,
            cell_site_location_area_code: None,
            cell_site_network_code: None,
            cell_site_type: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CellSiteFacetBuilder {
    cell_site_country_code: Option<String>,
    cell_site_identifier: Option<String>,
    cell_site_location_area_code: Option<String>,
    cell_site_network_code: Option<String>,
    cell_site_type: Option<String>,
}

impl CellSiteFacetBuilder {
    pub fn cell_site_country_code(mut self, value: String) -> Self {
        self.cell_site_country_code = Some(value);
        self
    }

    pub fn cell_site_identifier(mut self, value: String) -> Self {
        self.cell_site_identifier = Some(value);
        self
    }

    pub fn cell_site_location_area_code(mut self, value: String) -> Self {
        self.cell_site_location_area_code = Some(value);
        self
    }

    pub fn cell_site_network_code(mut self, value: String) -> Self {
        self.cell_site_network_code = Some(value);
        self
    }

    pub fn cell_site_type(mut self, value: String) -> Self {
        self.cell_site_type = Some(value);
        self
    }

    pub fn build(self) -> CellSiteFacet {
        CellSiteFacet {
            class_iri: CellSiteFacet::CLASS_IRI,
            cell_site_country_code: self.cell_site_country_code,
            cell_site_identifier: self.cell_site_identifier,
            cell_site_location_area_code: self.cell_site_location_area_code,
            cell_site_network_code: self.cell_site_network_code,
            cell_site_type: self.cell_site_type,
        }
    }
}

impl CaseObject for CellSiteFacet {
    fn class_iri() -> &'static str { CellSiteFacet::CLASS_IRI }
    fn type_name() -> &'static str { "CellSiteFacet" }
}

/// A character device node is a UNIX filesystem special file that serves as a conduit to communicate with devices, providing only a serial stream of input or accepting a serial stream of output. Characte
#[derive(Debug, Clone, Serialize)]
pub struct CharacterDeviceNode {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl CharacterDeviceNode {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/CharacterDeviceNode";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> CharacterDeviceNodeBuilder {
        CharacterDeviceNodeBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CharacterDeviceNodeBuilder {
}

impl CharacterDeviceNodeBuilder {
    pub fn build(self) -> CharacterDeviceNode {
        CharacterDeviceNode {
            class_iri: CharacterDeviceNode::CLASS_IRI,
        }
    }
}

impl CaseObject for CharacterDeviceNode {
    fn class_iri() -> &'static str { CharacterDeviceNode::CLASS_IRI }
    fn type_name() -> &'static str { "CharacterDeviceNode" }
}

/// Code is a direct representation (source, byte or binary) of a collection of computer instructions that form software which tell a computer how to work. [based on https://en.wikipedia.org/wiki/Software
#[derive(Debug, Clone, Serialize)]
pub struct Code {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Code {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Code";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> CodeBuilder {
        CodeBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CodeBuilder {
}

impl CodeBuilder {
    pub fn build(self) -> Code {
        Code {
            class_iri: Code::CLASS_IRI,
        }
    }
}

impl CaseObject for Code {
    fn class_iri() -> &'static str { Code::CLASS_IRI }
    fn type_name() -> &'static str { "Code" }
}

/// A compressed stream facet is a grouping of characteristics unique to the application of a size-reduction process to a body of data content.
#[derive(Debug, Clone, Serialize)]
pub struct CompressedStreamFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:compressionMethod")]
    pub compression_method: Option<String>,
    #[serde(rename = "uco-observable:compressionRatio")]
    pub compression_ratio: Option<f64>,
}

impl CompressedStreamFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/CompressedStreamFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> CompressedStreamFacetBuilder {
        CompressedStreamFacetBuilder {
            compression_method: None,
            compression_ratio: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CompressedStreamFacetBuilder {
    compression_method: Option<String>,
    compression_ratio: Option<f64>,
}

impl CompressedStreamFacetBuilder {
    pub fn compression_method(mut self, value: String) -> Self {
        self.compression_method = Some(value);
        self
    }

    pub fn compression_ratio(mut self, value: f64) -> Self {
        self.compression_ratio = Some(value);
        self
    }

    pub fn build(self) -> CompressedStreamFacet {
        CompressedStreamFacet {
            class_iri: CompressedStreamFacet::CLASS_IRI,
            compression_method: self.compression_method,
            compression_ratio: self.compression_ratio,
        }
    }
}

impl CaseObject for CompressedStreamFacet {
    fn class_iri() -> &'static str { CompressedStreamFacet::CLASS_IRI }
    fn type_name() -> &'static str { "CompressedStreamFacet" }
}

/// A computer is an electronic device for storing and processing data, typically in binary, according to instructions given to it in a variable program. [based on 'Computer.' Oxford English Dictionary, O
#[derive(Debug, Clone, Serialize)]
pub struct Computer {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Computer {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Computer";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ComputerBuilder {
        ComputerBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ComputerBuilder {
}

impl ComputerBuilder {
    pub fn build(self) -> Computer {
        Computer {
            class_iri: Computer::CLASS_IRI,
        }
    }
}

impl CaseObject for Computer {
    fn class_iri() -> &'static str { Computer::CLASS_IRI }
    fn type_name() -> &'static str { "Computer" }
}

/// A computer specification is the hardware and software of a programmable electronic device that can store, retrieve, and process data. {based on merriam-webster.com/dictionary/computer]
#[derive(Debug, Clone, Serialize)]
pub struct ComputerSpecification {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ComputerSpecification {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ComputerSpecification";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ComputerSpecificationBuilder {
        ComputerSpecificationBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ComputerSpecificationBuilder {
}

impl ComputerSpecificationBuilder {
    pub fn build(self) -> ComputerSpecification {
        ComputerSpecification {
            class_iri: ComputerSpecification::CLASS_IRI,
        }
    }
}

impl CaseObject for ComputerSpecification {
    fn class_iri() -> &'static str { ComputerSpecification::CLASS_IRI }
    fn type_name() -> &'static str { "ComputerSpecification" }
}

/// A computer specificaiton facet is a grouping of characteristics unique to the hardware and software of a programmable electronic device that can store, retrieve, and process data. [based on merriam-we
#[derive(Debug, Clone, Serialize)]
pub struct ComputerSpecificationFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:availableRam")]
    pub available_ram: Option<i64>,
    #[serde(rename = "uco-observable:biosDate")]
    pub bios_date: Option<String>,
    #[serde(rename = "uco-observable:biosManufacturer")]
    pub bios_manufacturer: Option<String>,
    #[serde(rename = "uco-observable:biosReleaseDate")]
    pub bios_release_date: Option<String>,
    #[serde(rename = "uco-observable:biosSerialNumber")]
    pub bios_serial_number: Option<String>,
    #[serde(rename = "uco-observable:biosVersion")]
    pub bios_version: Option<String>,
    #[serde(rename = "uco-observable:cpu")]
    pub cpu: Option<String>,
    #[serde(rename = "uco-observable:cpuFamily")]
    pub cpu_family: Option<String>,
    #[serde(rename = "uco-observable:currentSystemDate")]
    pub current_system_date: Option<String>,
    #[serde(rename = "uco-observable:gpu")]
    pub gpu: Option<String>,
    #[serde(rename = "uco-observable:gpuFamily")]
    pub gpu_family: Option<String>,
    #[serde(rename = "uco-observable:hostname")]
    pub hostname: Option<String>,
    #[serde(rename = "uco-observable:localTime")]
    pub local_time: Option<String>,
    #[serde(rename = "uco-observable:networkInterface")]
    pub network_interface: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:processorArchitecture")]
    pub processor_architecture: Option<String>,
    #[serde(rename = "uco-observable:systemTime")]
    pub system_time: Option<String>,
    #[serde(rename = "uco-observable:timezoneDST")]
    pub timezone_dst: Option<String>,
    #[serde(rename = "uco-observable:timezoneStandard")]
    pub timezone_standard: Option<String>,
    #[serde(rename = "uco-observable:totalRam")]
    pub total_ram: Option<i64>,
    #[serde(rename = "uco-observable:uptime")]
    pub uptime: Option<String>,
}

impl ComputerSpecificationFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ComputerSpecificationFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ComputerSpecificationFacetBuilder {
        ComputerSpecificationFacetBuilder {
            available_ram: None,
            bios_date: None,
            bios_manufacturer: None,
            bios_release_date: None,
            bios_serial_number: None,
            bios_version: None,
            cpu: None,
            cpu_family: None,
            current_system_date: None,
            gpu: None,
            gpu_family: None,
            hostname: None,
            local_time: None,
            network_interface: Vec::new(),
            processor_architecture: None,
            system_time: None,
            timezone_dst: None,
            timezone_standard: None,
            total_ram: None,
            uptime: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ComputerSpecificationFacetBuilder {
    available_ram: Option<i64>,
    bios_date: Option<String>,
    bios_manufacturer: Option<String>,
    bios_release_date: Option<String>,
    bios_serial_number: Option<String>,
    bios_version: Option<String>,
    cpu: Option<String>,
    cpu_family: Option<String>,
    current_system_date: Option<String>,
    gpu: Option<String>,
    gpu_family: Option<String>,
    hostname: Option<String>,
    local_time: Option<String>,
    network_interface: Vec<ObservableObject>,
    processor_architecture: Option<String>,
    system_time: Option<String>,
    timezone_dst: Option<String>,
    timezone_standard: Option<String>,
    total_ram: Option<i64>,
    uptime: Option<String>,
}

impl ComputerSpecificationFacetBuilder {
    pub fn available_ram(mut self, value: i64) -> Self {
        self.available_ram = Some(value);
        self
    }

    pub fn bios_date(mut self, value: String) -> Self {
        self.bios_date = Some(value);
        self
    }

    pub fn bios_manufacturer(mut self, value: String) -> Self {
        self.bios_manufacturer = Some(value);
        self
    }

    pub fn bios_release_date(mut self, value: String) -> Self {
        self.bios_release_date = Some(value);
        self
    }

    pub fn bios_serial_number(mut self, value: String) -> Self {
        self.bios_serial_number = Some(value);
        self
    }

    pub fn bios_version(mut self, value: String) -> Self {
        self.bios_version = Some(value);
        self
    }

    pub fn cpu(mut self, value: String) -> Self {
        self.cpu = Some(value);
        self
    }

    pub fn cpu_family(mut self, value: String) -> Self {
        self.cpu_family = Some(value);
        self
    }

    pub fn current_system_date(mut self, value: String) -> Self {
        self.current_system_date = Some(value);
        self
    }

    pub fn gpu(mut self, value: String) -> Self {
        self.gpu = Some(value);
        self
    }

    pub fn gpu_family(mut self, value: String) -> Self {
        self.gpu_family = Some(value);
        self
    }

    pub fn hostname(mut self, value: String) -> Self {
        self.hostname = Some(value);
        self
    }

    pub fn local_time(mut self, value: String) -> Self {
        self.local_time = Some(value);
        self
    }

    pub fn network_interface(mut self, value: Vec<ObservableObject>) -> Self {
        self.network_interface = value;
        self
    }

    pub fn processor_architecture(mut self, value: String) -> Self {
        self.processor_architecture = Some(value);
        self
    }

    pub fn system_time(mut self, value: String) -> Self {
        self.system_time = Some(value);
        self
    }

    pub fn timezone_dst(mut self, value: String) -> Self {
        self.timezone_dst = Some(value);
        self
    }

    pub fn timezone_standard(mut self, value: String) -> Self {
        self.timezone_standard = Some(value);
        self
    }

    pub fn total_ram(mut self, value: i64) -> Self {
        self.total_ram = Some(value);
        self
    }

    pub fn uptime(mut self, value: String) -> Self {
        self.uptime = Some(value);
        self
    }

    pub fn build(self) -> ComputerSpecificationFacet {
        ComputerSpecificationFacet {
            class_iri: ComputerSpecificationFacet::CLASS_IRI,
            available_ram: self.available_ram,
            bios_date: self.bios_date,
            bios_manufacturer: self.bios_manufacturer,
            bios_release_date: self.bios_release_date,
            bios_serial_number: self.bios_serial_number,
            bios_version: self.bios_version,
            cpu: self.cpu,
            cpu_family: self.cpu_family,
            current_system_date: self.current_system_date,
            gpu: self.gpu,
            gpu_family: self.gpu_family,
            hostname: self.hostname,
            local_time: self.local_time,
            network_interface: self.network_interface,
            processor_architecture: self.processor_architecture,
            system_time: self.system_time,
            timezone_dst: self.timezone_dst,
            timezone_standard: self.timezone_standard,
            total_ram: self.total_ram,
            uptime: self.uptime,
        }
    }
}

impl CaseObject for ComputerSpecificationFacet {
    fn class_iri() -> &'static str { ComputerSpecificationFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ComputerSpecificationFacet" }
}

/// A ConfiguredSoftware is a Software that is known to be configured to run in a more specified manner than some unconfigured or less-configured Software.
#[derive(Debug, Clone, Serialize)]
pub struct ConfiguredSoftware {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-configuration:isConfigurationOf")]
    pub is_configuration_of: Option<Software>,
    #[serde(rename = "uco-configuration:usesConfiguration")]
    pub uses_configuration: Option<Configuration>,
}

impl ConfiguredSoftware {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ConfiguredSoftware";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ConfiguredSoftwareBuilder {
        ConfiguredSoftwareBuilder {
            is_configuration_of: None,
            uses_configuration: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ConfiguredSoftwareBuilder {
    is_configuration_of: Option<Software>,
    uses_configuration: Option<Configuration>,
}

impl ConfiguredSoftwareBuilder {
    pub fn is_configuration_of(mut self, value: Software) -> Self {
        self.is_configuration_of = Some(value);
        self
    }

    pub fn uses_configuration(mut self, value: Configuration) -> Self {
        self.uses_configuration = Some(value);
        self
    }

    pub fn build(self) -> ConfiguredSoftware {
        ConfiguredSoftware {
            class_iri: ConfiguredSoftware::CLASS_IRI,
            is_configuration_of: self.is_configuration_of,
            uses_configuration: self.uses_configuration,
        }
    }
}

impl CaseObject for ConfiguredSoftware {
    fn class_iri() -> &'static str { ConfiguredSoftware::CLASS_IRI }
    fn type_name() -> &'static str { "ConfiguredSoftware" }
}

/// A contact is a set of identification and communication related details for a single entity.
#[derive(Debug, Clone, Serialize)]
pub struct Contact {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Contact {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Contact";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ContactBuilder {
        ContactBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ContactBuilder {
}

impl ContactBuilder {
    pub fn build(self) -> Contact {
        Contact {
            class_iri: Contact::CLASS_IRI,
        }
    }
}

impl CaseObject for Contact {
    fn class_iri() -> &'static str { Contact::CLASS_IRI }
    fn type_name() -> &'static str { "Contact" }
}

/// A contact address is a grouping of characteristics unique to a geolocation address of a contact entity.
#[derive(Debug, Clone, Serialize)]
pub struct ContactAddress {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:contactAddressScope")]
    pub contact_address_scope: Vec<String>,
    #[serde(rename = "uco-observable:geolocationAddress")]
    pub geolocation_address: Option<Location>,
}

impl ContactAddress {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactAddress";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ContactAddressBuilder {
        ContactAddressBuilder {
            contact_address_scope: Vec::new(),
            geolocation_address: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ContactAddressBuilder {
    contact_address_scope: Vec<String>,
    geolocation_address: Option<Location>,
}

impl ContactAddressBuilder {
    pub fn contact_address_scope(mut self, value: Vec<String>) -> Self {
        self.contact_address_scope = value;
        self
    }

    pub fn geolocation_address(mut self, value: Location) -> Self {
        self.geolocation_address = Some(value);
        self
    }

    pub fn build(self) -> ContactAddress {
        ContactAddress {
            class_iri: ContactAddress::CLASS_IRI,
            contact_address_scope: self.contact_address_scope,
            geolocation_address: self.geolocation_address,
        }
    }
}

impl CaseObject for ContactAddress {
    fn class_iri() -> &'static str { ContactAddress::CLASS_IRI }
    fn type_name() -> &'static str { "ContactAddress" }
}

/// A contact affiliation is a grouping of characteristics unique to details of an organizational affiliation for a single contact entity.
#[derive(Debug, Clone, Serialize)]
pub struct ContactAffiliation {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:contactEmail")]
    pub contact_email: Vec<ContactEmail>,
    #[serde(rename = "uco-observable:contactMessaging")]
    pub contact_messaging: Vec<ContactMessaging>,
    #[serde(rename = "uco-observable:contactOrganization")]
    pub contact_organization: Option<Organization>,
    #[serde(rename = "uco-observable:contactPhone")]
    pub contact_phone: Vec<ContactPhone>,
    #[serde(rename = "uco-observable:contactProfile")]
    pub contact_profile: Vec<ContactProfile>,
    #[serde(rename = "uco-observable:contactURL")]
    pub contact_url: Vec<ContactURL>,
    #[serde(rename = "uco-observable:organizationDepartment")]
    pub organization_department: Option<String>,
    #[serde(rename = "uco-observable:organizationLocation")]
    pub organization_location: Vec<ContactAddress>,
    #[serde(rename = "uco-observable:organizationPosition")]
    pub organization_position: Option<String>,
}

impl ContactAffiliation {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactAffiliation";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ContactAffiliationBuilder {
        ContactAffiliationBuilder {
            contact_email: Vec::new(),
            contact_messaging: Vec::new(),
            contact_organization: None,
            contact_phone: Vec::new(),
            contact_profile: Vec::new(),
            contact_url: Vec::new(),
            organization_department: None,
            organization_location: Vec::new(),
            organization_position: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ContactAffiliationBuilder {
    contact_email: Vec<ContactEmail>,
    contact_messaging: Vec<ContactMessaging>,
    contact_organization: Option<Organization>,
    contact_phone: Vec<ContactPhone>,
    contact_profile: Vec<ContactProfile>,
    contact_url: Vec<ContactURL>,
    organization_department: Option<String>,
    organization_location: Vec<ContactAddress>,
    organization_position: Option<String>,
}

impl ContactAffiliationBuilder {
    pub fn contact_email(mut self, value: Vec<ContactEmail>) -> Self {
        self.contact_email = value;
        self
    }

    pub fn contact_messaging(mut self, value: Vec<ContactMessaging>) -> Self {
        self.contact_messaging = value;
        self
    }

    pub fn contact_organization(mut self, value: Organization) -> Self {
        self.contact_organization = Some(value);
        self
    }

    pub fn contact_phone(mut self, value: Vec<ContactPhone>) -> Self {
        self.contact_phone = value;
        self
    }

    pub fn contact_profile(mut self, value: Vec<ContactProfile>) -> Self {
        self.contact_profile = value;
        self
    }

    pub fn contact_url(mut self, value: Vec<ContactURL>) -> Self {
        self.contact_url = value;
        self
    }

    pub fn organization_department(mut self, value: String) -> Self {
        self.organization_department = Some(value);
        self
    }

    pub fn organization_location(mut self, value: Vec<ContactAddress>) -> Self {
        self.organization_location = value;
        self
    }

    pub fn organization_position(mut self, value: String) -> Self {
        self.organization_position = Some(value);
        self
    }

    pub fn build(self) -> ContactAffiliation {
        ContactAffiliation {
            class_iri: ContactAffiliation::CLASS_IRI,
            contact_email: self.contact_email,
            contact_messaging: self.contact_messaging,
            contact_organization: self.contact_organization,
            contact_phone: self.contact_phone,
            contact_profile: self.contact_profile,
            contact_url: self.contact_url,
            organization_department: self.organization_department,
            organization_location: self.organization_location,
            organization_position: self.organization_position,
        }
    }
}

impl CaseObject for ContactAffiliation {
    fn class_iri() -> &'static str { ContactAffiliation::CLASS_IRI }
    fn type_name() -> &'static str { "ContactAffiliation" }
}

/// A contact email is a grouping of characteristics unique to details for contacting a contact entity by email.
#[derive(Debug, Clone, Serialize)]
pub struct ContactEmail {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:contactEmailScope")]
    pub contact_email_scope: Vec<String>,
    #[serde(rename = "uco-observable:emailAddress")]
    pub email_address: Option<ObservableObject>,
}

impl ContactEmail {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactEmail";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ContactEmailBuilder {
        ContactEmailBuilder {
            contact_email_scope: Vec::new(),
            email_address: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ContactEmailBuilder {
    contact_email_scope: Vec<String>,
    email_address: Option<ObservableObject>,
}

impl ContactEmailBuilder {
    pub fn contact_email_scope(mut self, value: Vec<String>) -> Self {
        self.contact_email_scope = value;
        self
    }

    pub fn email_address(mut self, value: ObservableObject) -> Self {
        self.email_address = Some(value);
        self
    }

    pub fn build(self) -> ContactEmail {
        ContactEmail {
            class_iri: ContactEmail::CLASS_IRI,
            contact_email_scope: self.contact_email_scope,
            email_address: self.email_address,
        }
    }
}

impl CaseObject for ContactEmail {
    fn class_iri() -> &'static str { ContactEmail::CLASS_IRI }
    fn type_name() -> &'static str { "ContactEmail" }
}

/// A contact facet is a grouping of characteristics unique to a set of identification and communication related details for a single entity.
#[derive(Debug, Clone, Serialize)]
pub struct ContactFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-identity:birthdate")]
    pub birthdate: Option<String>,
    #[serde(rename = "uco-observable:contactAddress")]
    pub contact_address: Vec<ContactAddress>,
    #[serde(rename = "uco-observable:contactAffiliation")]
    pub contact_affiliation: Vec<ContactAffiliation>,
    #[serde(rename = "uco-observable:contactEmail")]
    pub contact_email: Vec<ContactEmail>,
    #[serde(rename = "uco-observable:contactGroup")]
    pub contact_group: Vec<String>,
    #[serde(rename = "uco-observable:contactID")]
    pub contact_id: Option<String>,
    #[serde(rename = "uco-observable:contactMessaging")]
    pub contact_messaging: Vec<ContactMessaging>,
    #[serde(rename = "uco-observable:contactNote")]
    pub contact_note: Vec<String>,
    #[serde(rename = "uco-observable:contactPhone")]
    pub contact_phone: Vec<ContactPhone>,
    #[serde(rename = "uco-observable:contactProfile")]
    pub contact_profile: Vec<ContactProfile>,
    #[serde(rename = "uco-observable:contactSIP")]
    pub contact_sip: Vec<ContactSIP>,
    #[serde(rename = "uco-observable:contactURL")]
    pub contact_url: Vec<ContactURL>,
    #[serde(rename = "uco-observable:displayName")]
    pub display_name: Option<String>,
    #[serde(rename = "uco-observable:firstName")]
    pub first_name: Option<String>,
    #[serde(rename = "uco-observable:lastName")]
    pub last_name: Option<String>,
    #[serde(rename = "uco-observable:lastTimeContacted")]
    pub last_time_contacted: Option<String>,
    #[serde(rename = "uco-observable:middleName")]
    pub middle_name: Option<String>,
    #[serde(rename = "uco-observable:namePhonetic")]
    pub name_phonetic: Option<String>,
    #[serde(rename = "uco-observable:namePrefix")]
    pub name_prefix: Option<String>,
    #[serde(rename = "uco-observable:nameSuffix")]
    pub name_suffix: Option<String>,
    #[serde(rename = "uco-observable:nickname")]
    pub nickname: Vec<String>,
    #[serde(rename = "uco-observable:numberTimesContacted")]
    pub number_times_contacted: Option<i64>,
    #[serde(rename = "uco-observable:sourceApplication")]
    pub source_application: Option<ObservableObject>,
}

impl ContactFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ContactFacetBuilder {
        ContactFacetBuilder {
            birthdate: None,
            contact_address: Vec::new(),
            contact_affiliation: Vec::new(),
            contact_email: Vec::new(),
            contact_group: Vec::new(),
            contact_id: None,
            contact_messaging: Vec::new(),
            contact_note: Vec::new(),
            contact_phone: Vec::new(),
            contact_profile: Vec::new(),
            contact_sip: Vec::new(),
            contact_url: Vec::new(),
            display_name: None,
            first_name: None,
            last_name: None,
            last_time_contacted: None,
            middle_name: None,
            name_phonetic: None,
            name_prefix: None,
            name_suffix: None,
            nickname: Vec::new(),
            number_times_contacted: None,
            source_application: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ContactFacetBuilder {
    birthdate: Option<String>,
    contact_address: Vec<ContactAddress>,
    contact_affiliation: Vec<ContactAffiliation>,
    contact_email: Vec<ContactEmail>,
    contact_group: Vec<String>,
    contact_id: Option<String>,
    contact_messaging: Vec<ContactMessaging>,
    contact_note: Vec<String>,
    contact_phone: Vec<ContactPhone>,
    contact_profile: Vec<ContactProfile>,
    contact_sip: Vec<ContactSIP>,
    contact_url: Vec<ContactURL>,
    display_name: Option<String>,
    first_name: Option<String>,
    last_name: Option<String>,
    last_time_contacted: Option<String>,
    middle_name: Option<String>,
    name_phonetic: Option<String>,
    name_prefix: Option<String>,
    name_suffix: Option<String>,
    nickname: Vec<String>,
    number_times_contacted: Option<i64>,
    source_application: Option<ObservableObject>,
}

impl ContactFacetBuilder {
    pub fn birthdate(mut self, value: String) -> Self {
        self.birthdate = Some(value);
        self
    }

    pub fn contact_address(mut self, value: Vec<ContactAddress>) -> Self {
        self.contact_address = value;
        self
    }

    pub fn contact_affiliation(mut self, value: Vec<ContactAffiliation>) -> Self {
        self.contact_affiliation = value;
        self
    }

    pub fn contact_email(mut self, value: Vec<ContactEmail>) -> Self {
        self.contact_email = value;
        self
    }

    pub fn contact_group(mut self, value: Vec<String>) -> Self {
        self.contact_group = value;
        self
    }

    pub fn contact_id(mut self, value: String) -> Self {
        self.contact_id = Some(value);
        self
    }

    pub fn contact_messaging(mut self, value: Vec<ContactMessaging>) -> Self {
        self.contact_messaging = value;
        self
    }

    pub fn contact_note(mut self, value: Vec<String>) -> Self {
        self.contact_note = value;
        self
    }

    pub fn contact_phone(mut self, value: Vec<ContactPhone>) -> Self {
        self.contact_phone = value;
        self
    }

    pub fn contact_profile(mut self, value: Vec<ContactProfile>) -> Self {
        self.contact_profile = value;
        self
    }

    pub fn contact_sip(mut self, value: Vec<ContactSIP>) -> Self {
        self.contact_sip = value;
        self
    }

    pub fn contact_url(mut self, value: Vec<ContactURL>) -> Self {
        self.contact_url = value;
        self
    }

    pub fn display_name(mut self, value: String) -> Self {
        self.display_name = Some(value);
        self
    }

    pub fn first_name(mut self, value: String) -> Self {
        self.first_name = Some(value);
        self
    }

    pub fn last_name(mut self, value: String) -> Self {
        self.last_name = Some(value);
        self
    }

    pub fn last_time_contacted(mut self, value: String) -> Self {
        self.last_time_contacted = Some(value);
        self
    }

    pub fn middle_name(mut self, value: String) -> Self {
        self.middle_name = Some(value);
        self
    }

    pub fn name_phonetic(mut self, value: String) -> Self {
        self.name_phonetic = Some(value);
        self
    }

    pub fn name_prefix(mut self, value: String) -> Self {
        self.name_prefix = Some(value);
        self
    }

    pub fn name_suffix(mut self, value: String) -> Self {
        self.name_suffix = Some(value);
        self
    }

    pub fn nickname(mut self, value: Vec<String>) -> Self {
        self.nickname = value;
        self
    }

    pub fn number_times_contacted(mut self, value: i64) -> Self {
        self.number_times_contacted = Some(value);
        self
    }

    pub fn source_application(mut self, value: ObservableObject) -> Self {
        self.source_application = Some(value);
        self
    }

    pub fn build(self) -> ContactFacet {
        ContactFacet {
            class_iri: ContactFacet::CLASS_IRI,
            birthdate: self.birthdate,
            contact_address: self.contact_address,
            contact_affiliation: self.contact_affiliation,
            contact_email: self.contact_email,
            contact_group: self.contact_group,
            contact_id: self.contact_id,
            contact_messaging: self.contact_messaging,
            contact_note: self.contact_note,
            contact_phone: self.contact_phone,
            contact_profile: self.contact_profile,
            contact_sip: self.contact_sip,
            contact_url: self.contact_url,
            display_name: self.display_name,
            first_name: self.first_name,
            last_name: self.last_name,
            last_time_contacted: self.last_time_contacted,
            middle_name: self.middle_name,
            name_phonetic: self.name_phonetic,
            name_prefix: self.name_prefix,
            name_suffix: self.name_suffix,
            nickname: self.nickname,
            number_times_contacted: self.number_times_contacted,
            source_application: self.source_application,
        }
    }
}

impl CaseObject for ContactFacet {
    fn class_iri() -> &'static str { ContactFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ContactFacet" }
}

/// A contact list is a set of multiple individual contacts such as that found in a digital address book.
#[derive(Debug, Clone, Serialize)]
pub struct ContactList {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ContactList {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactList";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ContactListBuilder {
        ContactListBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ContactListBuilder {
}

impl ContactListBuilder {
    pub fn build(self) -> ContactList {
        ContactList {
            class_iri: ContactList::CLASS_IRI,
        }
    }
}

impl CaseObject for ContactList {
    fn class_iri() -> &'static str { ContactList::CLASS_IRI }
    fn type_name() -> &'static str { "ContactList" }
}

/// A contact list facet is a grouping of characteristics unique to a set of multiple individual contacts such as that found in a digital address book.
#[derive(Debug, Clone, Serialize)]
pub struct ContactListFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:contact")]
    pub contact: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:sourceApplication")]
    pub source_application: Option<ObservableObject>,
}

impl ContactListFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactListFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ContactListFacetBuilder {
        ContactListFacetBuilder {
            contact: Vec::new(),
            source_application: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ContactListFacetBuilder {
    contact: Vec<ObservableObject>,
    source_application: Option<ObservableObject>,
}

impl ContactListFacetBuilder {
    pub fn contact(mut self, value: Vec<ObservableObject>) -> Self {
        self.contact = value;
        self
    }

    pub fn source_application(mut self, value: ObservableObject) -> Self {
        self.source_application = Some(value);
        self
    }

    pub fn build(self) -> ContactListFacet {
        ContactListFacet {
            class_iri: ContactListFacet::CLASS_IRI,
            contact: self.contact,
            source_application: self.source_application,
        }
    }
}

impl CaseObject for ContactListFacet {
    fn class_iri() -> &'static str { ContactListFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ContactListFacet" }
}

/// A contact messaging is a grouping of characteristics unique to details for contacting a contact entity by digital messaging.
#[derive(Debug, Clone, Serialize)]
pub struct ContactMessaging {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:contactMessagingPlatform")]
    pub contact_messaging_platform: Option<ObservableObject>,
    #[serde(rename = "uco-observable:messagingAddress")]
    pub messaging_address: Option<ObservableObject>,
}

impl ContactMessaging {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactMessaging";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ContactMessagingBuilder {
        ContactMessagingBuilder {
            contact_messaging_platform: None,
            messaging_address: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ContactMessagingBuilder {
    contact_messaging_platform: Option<ObservableObject>,
    messaging_address: Option<ObservableObject>,
}

impl ContactMessagingBuilder {
    pub fn contact_messaging_platform(mut self, value: ObservableObject) -> Self {
        self.contact_messaging_platform = Some(value);
        self
    }

    pub fn messaging_address(mut self, value: ObservableObject) -> Self {
        self.messaging_address = Some(value);
        self
    }

    pub fn build(self) -> ContactMessaging {
        ContactMessaging {
            class_iri: ContactMessaging::CLASS_IRI,
            contact_messaging_platform: self.contact_messaging_platform,
            messaging_address: self.messaging_address,
        }
    }
}

impl CaseObject for ContactMessaging {
    fn class_iri() -> &'static str { ContactMessaging::CLASS_IRI }
    fn type_name() -> &'static str { "ContactMessaging" }
}

/// A contact phone is a grouping of characteristics unique to details for contacting a contact entity by telephone.
#[derive(Debug, Clone, Serialize)]
pub struct ContactPhone {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:contactPhoneNumber")]
    pub contact_phone_number: Option<ObservableObject>,
    #[serde(rename = "uco-observable:contactPhoneScope")]
    pub contact_phone_scope: Vec<String>,
}

impl ContactPhone {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactPhone";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ContactPhoneBuilder {
        ContactPhoneBuilder {
            contact_phone_number: None,
            contact_phone_scope: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ContactPhoneBuilder {
    contact_phone_number: Option<ObservableObject>,
    contact_phone_scope: Vec<String>,
}

impl ContactPhoneBuilder {
    pub fn contact_phone_number(mut self, value: ObservableObject) -> Self {
        self.contact_phone_number = Some(value);
        self
    }

    pub fn contact_phone_scope(mut self, value: Vec<String>) -> Self {
        self.contact_phone_scope = value;
        self
    }

    pub fn build(self) -> ContactPhone {
        ContactPhone {
            class_iri: ContactPhone::CLASS_IRI,
            contact_phone_number: self.contact_phone_number,
            contact_phone_scope: self.contact_phone_scope,
        }
    }
}

impl CaseObject for ContactPhone {
    fn class_iri() -> &'static str { ContactPhone::CLASS_IRI }
    fn type_name() -> &'static str { "ContactPhone" }
}

/// A contact profile is a grouping of characteristics unique to details for contacting a contact entity by online service.
#[derive(Debug, Clone, Serialize)]
pub struct ContactProfile {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:contactProfilePlatform")]
    pub contact_profile_platform: Option<ObservableObject>,
    #[serde(rename = "uco-observable:profile")]
    pub profile: Option<ObservableObject>,
}

impl ContactProfile {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactProfile";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ContactProfileBuilder {
        ContactProfileBuilder {
            contact_profile_platform: None,
            profile: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ContactProfileBuilder {
    contact_profile_platform: Option<ObservableObject>,
    profile: Option<ObservableObject>,
}

impl ContactProfileBuilder {
    pub fn contact_profile_platform(mut self, value: ObservableObject) -> Self {
        self.contact_profile_platform = Some(value);
        self
    }

    pub fn profile(mut self, value: ObservableObject) -> Self {
        self.profile = Some(value);
        self
    }

    pub fn build(self) -> ContactProfile {
        ContactProfile {
            class_iri: ContactProfile::CLASS_IRI,
            contact_profile_platform: self.contact_profile_platform,
            profile: self.profile,
        }
    }
}

impl CaseObject for ContactProfile {
    fn class_iri() -> &'static str { ContactProfile::CLASS_IRI }
    fn type_name() -> &'static str { "ContactProfile" }
}

/// A contact SIP is a grouping of characteristics unique to details for contacting a contact entity by Session Initiation Protocol (SIP).
#[derive(Debug, Clone, Serialize)]
pub struct ContactSIP {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:contactSIPScope")]
    pub contact_sip_scope: Vec<String>,
    #[serde(rename = "uco-observable:sipAddress")]
    pub sip_address: Option<ObservableObject>,
}

impl ContactSIP {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactSIP";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ContactSIPBuilder {
        ContactSIPBuilder {
            contact_sip_scope: Vec::new(),
            sip_address: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ContactSIPBuilder {
    contact_sip_scope: Vec<String>,
    sip_address: Option<ObservableObject>,
}

impl ContactSIPBuilder {
    pub fn contact_sip_scope(mut self, value: Vec<String>) -> Self {
        self.contact_sip_scope = value;
        self
    }

    pub fn sip_address(mut self, value: ObservableObject) -> Self {
        self.sip_address = Some(value);
        self
    }

    pub fn build(self) -> ContactSIP {
        ContactSIP {
            class_iri: ContactSIP::CLASS_IRI,
            contact_sip_scope: self.contact_sip_scope,
            sip_address: self.sip_address,
        }
    }
}

impl CaseObject for ContactSIP {
    fn class_iri() -> &'static str { ContactSIP::CLASS_IRI }
    fn type_name() -> &'static str { "ContactSIP" }
}

/// A contact URL is a grouping of characteristics unique to details for contacting a contact entity by Uniform Resource Locator (URL).
#[derive(Debug, Clone, Serialize)]
pub struct ContactURL {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:contactURLScope")]
    pub contact_url_scope: Vec<String>,
    #[serde(rename = "uco-observable:url")]
    pub url: Option<ObservableObject>,
}

impl ContactURL {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ContactURL";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ContactURLBuilder {
        ContactURLBuilder {
            contact_url_scope: Vec::new(),
            url: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ContactURLBuilder {
    contact_url_scope: Vec<String>,
    url: Option<ObservableObject>,
}

impl ContactURLBuilder {
    pub fn contact_url_scope(mut self, value: Vec<String>) -> Self {
        self.contact_url_scope = value;
        self
    }

    pub fn url(mut self, value: ObservableObject) -> Self {
        self.url = Some(value);
        self
    }

    pub fn build(self) -> ContactURL {
        ContactURL {
            class_iri: ContactURL::CLASS_IRI,
            contact_url_scope: self.contact_url_scope,
            url: self.url,
        }
    }
}

impl CaseObject for ContactURL {
    fn class_iri() -> &'static str { ContactURL::CLASS_IRI }
    fn type_name() -> &'static str { "ContactURL" }
}

/// Content data is a block of digital data.
#[derive(Debug, Clone, Serialize)]
pub struct ContentData {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ContentData {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ContentData";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ContentDataBuilder {
        ContentDataBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ContentDataBuilder {
}

impl ContentDataBuilder {
    pub fn build(self) -> ContentData {
        ContentData {
            class_iri: ContentData::CLASS_IRI,
        }
    }
}

impl CaseObject for ContentData {
    fn class_iri() -> &'static str { ContentData::CLASS_IRI }
    fn type_name() -> &'static str { "ContentData" }
}

/// A content data facet is a grouping of characteristics unique to a block of digital data.
#[derive(Debug, Clone, Serialize)]
pub struct ContentDataFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:byteOrder")]
    pub byte_order: Vec<String>,
    #[serde(rename = "uco-observable:dataPayload")]
    pub data_payload: Option<String>,
    #[serde(rename = "uco-observable:dataPayloadReferenceURL")]
    pub data_payload_reference_url: Option<ObservableObject>,
    #[serde(rename = "uco-observable:entropy")]
    pub entropy: Option<f64>,
    #[serde(rename = "uco-observable:hash")]
    pub hash: Vec<Hash>,
    #[serde(rename = "uco-observable:isEncrypted")]
    pub is_encrypted: Option<bool>,
    #[serde(rename = "uco-observable:magicNumber")]
    pub magic_number: Option<String>,
    #[serde(rename = "uco-observable:mimeClass")]
    pub mime_class: Option<String>,
    #[serde(rename = "uco-observable:mimeType")]
    pub mime_type: Vec<String>,
    #[serde(rename = "uco-observable:sizeInBytes")]
    pub size_in_bytes: Option<i64>,
}

impl ContentDataFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ContentDataFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ContentDataFacetBuilder {
        ContentDataFacetBuilder {
            byte_order: Vec::new(),
            data_payload: None,
            data_payload_reference_url: None,
            entropy: None,
            hash: Vec::new(),
            is_encrypted: None,
            magic_number: None,
            mime_class: None,
            mime_type: Vec::new(),
            size_in_bytes: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ContentDataFacetBuilder {
    byte_order: Vec<String>,
    data_payload: Option<String>,
    data_payload_reference_url: Option<ObservableObject>,
    entropy: Option<f64>,
    hash: Vec<Hash>,
    is_encrypted: Option<bool>,
    magic_number: Option<String>,
    mime_class: Option<String>,
    mime_type: Vec<String>,
    size_in_bytes: Option<i64>,
}

impl ContentDataFacetBuilder {
    pub fn byte_order(mut self, value: Vec<String>) -> Self {
        self.byte_order = value;
        self
    }

    pub fn data_payload(mut self, value: String) -> Self {
        self.data_payload = Some(value);
        self
    }

    pub fn data_payload_reference_url(mut self, value: ObservableObject) -> Self {
        self.data_payload_reference_url = Some(value);
        self
    }

    pub fn entropy(mut self, value: f64) -> Self {
        self.entropy = Some(value);
        self
    }

    pub fn hash(mut self, value: Vec<Hash>) -> Self {
        self.hash = value;
        self
    }

    pub fn is_encrypted(mut self, value: bool) -> Self {
        self.is_encrypted = Some(value);
        self
    }

    pub fn magic_number(mut self, value: String) -> Self {
        self.magic_number = Some(value);
        self
    }

    pub fn mime_class(mut self, value: String) -> Self {
        self.mime_class = Some(value);
        self
    }

    pub fn mime_type(mut self, value: Vec<String>) -> Self {
        self.mime_type = value;
        self
    }

    pub fn size_in_bytes(mut self, value: i64) -> Self {
        self.size_in_bytes = Some(value);
        self
    }

    pub fn build(self) -> ContentDataFacet {
        ContentDataFacet {
            class_iri: ContentDataFacet::CLASS_IRI,
            byte_order: self.byte_order,
            data_payload: self.data_payload,
            data_payload_reference_url: self.data_payload_reference_url,
            entropy: self.entropy,
            hash: self.hash,
            is_encrypted: self.is_encrypted,
            magic_number: self.magic_number,
            mime_class: self.mime_class,
            mime_type: self.mime_type,
            size_in_bytes: self.size_in_bytes,
        }
    }
}

impl CaseObject for ContentDataFacet {
    fn class_iri() -> &'static str { ContentDataFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ContentDataFacet" }
}

/// A cookie history is the stored web cookie history for a particular web browser.
#[derive(Debug, Clone, Serialize)]
pub struct CookieHistory {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl CookieHistory {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/CookieHistory";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> CookieHistoryBuilder {
        CookieHistoryBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CookieHistoryBuilder {
}

impl CookieHistoryBuilder {
    pub fn build(self) -> CookieHistory {
        CookieHistory {
            class_iri: CookieHistory::CLASS_IRI,
        }
    }
}

impl CaseObject for CookieHistory {
    fn class_iri() -> &'static str { CookieHistory::CLASS_IRI }
    fn type_name() -> &'static str { "CookieHistory" }
}

/// A credential is a single specific login and password combination for authorization of access to a digital account or system.
#[derive(Debug, Clone, Serialize)]
pub struct Credential {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Credential {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Credential";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> CredentialBuilder {
        CredentialBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CredentialBuilder {
}

impl CredentialBuilder {
    pub fn build(self) -> Credential {
        Credential {
            class_iri: Credential::CLASS_IRI,
        }
    }
}

impl CaseObject for Credential {
    fn class_iri() -> &'static str { Credential::CLASS_IRI }
    fn type_name() -> &'static str { "Credential" }
}

/// A credential dump is a collection (typically forcibly extracted from a system) of specific login and password combinations for authorization of access to a digital account or system.
#[derive(Debug, Clone, Serialize)]
pub struct CredentialDump {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl CredentialDump {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/CredentialDump";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> CredentialDumpBuilder {
        CredentialDumpBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct CredentialDumpBuilder {
}

impl CredentialDumpBuilder {
    pub fn build(self) -> CredentialDump {
        CredentialDump {
            class_iri: CredentialDump::CLASS_IRI,
        }
    }
}

impl CaseObject for CredentialDump {
    fn class_iri() -> &'static str { CredentialDump::CLASS_IRI }
    fn type_name() -> &'static str { "CredentialDump" }
}

/// An DNS cache is a temporary locally stored collection of previous Domain Name System (DNS) query results (created when an domain name is resolved to a IP address) for a particular computer.
#[derive(Debug, Clone, Serialize)]
pub struct DNSCache {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl DNSCache {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DNSCache";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DNSCacheBuilder {
        DNSCacheBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DNSCacheBuilder {
}

impl DNSCacheBuilder {
    pub fn build(self) -> DNSCache {
        DNSCache {
            class_iri: DNSCache::CLASS_IRI,
        }
    }
}

impl CaseObject for DNSCache {
    fn class_iri() -> &'static str { DNSCache::CLASS_IRI }
    fn type_name() -> &'static str { "DNSCache" }
}

/// A DNS record is a single Domain Name System (DNS) artifact specifying information of a particular type (routing, authority, responsibility, security, etc.) for a specific Internet domain name.
#[derive(Debug, Clone, Serialize)]
pub struct DNSRecord {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl DNSRecord {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DNSRecord";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DNSRecordBuilder {
        DNSRecordBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DNSRecordBuilder {
}

impl DNSRecordBuilder {
    pub fn build(self) -> DNSRecord {
        DNSRecord {
            class_iri: DNSRecord::CLASS_IRI,
        }
    }
}

impl CaseObject for DNSRecord {
    fn class_iri() -> &'static str { DNSRecord::CLASS_IRI }
    fn type_name() -> &'static str { "DNSRecord" }
}

/// A data range facet is a grouping of characteristics unique to a particular contiguous scope within a block of digital data.
#[derive(Debug, Clone, Serialize)]
pub struct DataRangeFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:rangeOffset")]
    pub range_offset: Option<i64>,
    #[serde(rename = "uco-observable:rangeOffsetType")]
    pub range_offset_type: Option<String>,
    #[serde(rename = "uco-observable:rangeSize")]
    pub range_size: Option<i64>,
}

impl DataRangeFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DataRangeFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DataRangeFacetBuilder {
        DataRangeFacetBuilder {
            range_offset: None,
            range_offset_type: None,
            range_size: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DataRangeFacetBuilder {
    range_offset: Option<i64>,
    range_offset_type: Option<String>,
    range_size: Option<i64>,
}

impl DataRangeFacetBuilder {
    pub fn range_offset(mut self, value: i64) -> Self {
        self.range_offset = Some(value);
        self
    }

    pub fn range_offset_type(mut self, value: String) -> Self {
        self.range_offset_type = Some(value);
        self
    }

    pub fn range_size(mut self, value: i64) -> Self {
        self.range_size = Some(value);
        self
    }

    pub fn build(self) -> DataRangeFacet {
        DataRangeFacet {
            class_iri: DataRangeFacet::CLASS_IRI,
            range_offset: self.range_offset,
            range_offset_type: self.range_offset_type,
            range_size: self.range_size,
        }
    }
}

impl CaseObject for DataRangeFacet {
    fn class_iri() -> &'static str { DataRangeFacet::CLASS_IRI }
    fn type_name() -> &'static str { "DataRangeFacet" }
}

/// A defined effect facet is a grouping of characteristics unique to the effect of an observable action in relation to one or more observable objects.
#[derive(Debug, Clone, Serialize)]
pub struct DefinedEffectFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl DefinedEffectFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DefinedEffectFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DefinedEffectFacetBuilder {
        DefinedEffectFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DefinedEffectFacetBuilder {
}

impl DefinedEffectFacetBuilder {
    pub fn build(self) -> DefinedEffectFacet {
        DefinedEffectFacet {
            class_iri: DefinedEffectFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for DefinedEffectFacet {
    fn class_iri() -> &'static str { DefinedEffectFacet::CLASS_IRI }
    fn type_name() -> &'static str { "DefinedEffectFacet" }
}

/// A device is a piece of equipment or a mechanism designed to serve a special purpose or perform a special function. [based on https://www.merriam-webster.com/dictionary/device]
#[derive(Debug, Clone, Serialize)]
pub struct Device {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Device {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Device";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DeviceBuilder {
        DeviceBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DeviceBuilder {
}

impl DeviceBuilder {
    pub fn build(self) -> Device {
        Device {
            class_iri: Device::CLASS_IRI,
        }
    }
}

impl CaseObject for Device {
    fn class_iri() -> &'static str { Device::CLASS_IRI }
    fn type_name() -> &'static str { "Device" }
}

/// A device facet is a grouping of characteristics unique to a piece of equipment or a mechanism designed to serve a special purpose or perform a special function. [based on https://www.merriam-webster.c
#[derive(Debug, Clone, Serialize)]
pub struct DeviceFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:cpeid")]
    pub cpeid: Option<String>,
    #[serde(rename = "uco-observable:deviceType")]
    pub device_type: Option<String>,
    #[serde(rename = "uco-observable:manufacturer")]
    pub manufacturer: Option<Identity>,
    #[serde(rename = "uco-observable:model")]
    pub model: Option<String>,
    #[serde(rename = "uco-observable:serialNumber")]
    pub serial_number: Option<String>,
}

impl DeviceFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DeviceFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DeviceFacetBuilder {
        DeviceFacetBuilder {
            cpeid: None,
            device_type: None,
            manufacturer: None,
            model: None,
            serial_number: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DeviceFacetBuilder {
    cpeid: Option<String>,
    device_type: Option<String>,
    manufacturer: Option<Identity>,
    model: Option<String>,
    serial_number: Option<String>,
}

impl DeviceFacetBuilder {
    pub fn cpeid(mut self, value: String) -> Self {
        self.cpeid = Some(value);
        self
    }

    pub fn device_type(mut self, value: String) -> Self {
        self.device_type = Some(value);
        self
    }

    pub fn manufacturer(mut self, value: Identity) -> Self {
        self.manufacturer = Some(value);
        self
    }

    pub fn model(mut self, value: String) -> Self {
        self.model = Some(value);
        self
    }

    pub fn serial_number(mut self, value: String) -> Self {
        self.serial_number = Some(value);
        self
    }

    pub fn build(self) -> DeviceFacet {
        DeviceFacet {
            class_iri: DeviceFacet::CLASS_IRI,
            cpeid: self.cpeid,
            device_type: self.device_type,
            manufacturer: self.manufacturer,
            model: self.model,
            serial_number: self.serial_number,
        }
    }
}

impl CaseObject for DeviceFacet {
    fn class_iri() -> &'static str { DeviceFacet::CLASS_IRI }
    fn type_name() -> &'static str { "DeviceFacet" }
}

/// A digital account is an arrangement with an entity to enable and control the provision of some capability or service within the digital domain.
#[derive(Debug, Clone, Serialize)]
pub struct DigitalAccount {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl DigitalAccount {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalAccount";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DigitalAccountBuilder {
        DigitalAccountBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DigitalAccountBuilder {
}

impl DigitalAccountBuilder {
    pub fn build(self) -> DigitalAccount {
        DigitalAccount {
            class_iri: DigitalAccount::CLASS_IRI,
        }
    }
}

impl CaseObject for DigitalAccount {
    fn class_iri() -> &'static str { DigitalAccount::CLASS_IRI }
    fn type_name() -> &'static str { "DigitalAccount" }
}

/// A digital account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of some capability or service within the digital domain.
#[derive(Debug, Clone, Serialize)]
pub struct DigitalAccountFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:accountLogin")]
    pub account_login: Vec<String>,
    #[serde(rename = "uco-observable:displayName")]
    pub display_name: Option<String>,
    #[serde(rename = "uco-observable:firstLoginTime")]
    pub first_login_time: Option<String>,
    #[serde(rename = "uco-observable:isDisabled")]
    pub is_disabled: Option<bool>,
    #[serde(rename = "uco-observable:lastLoginTime")]
    pub last_login_time: Option<String>,
}

impl DigitalAccountFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalAccountFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DigitalAccountFacetBuilder {
        DigitalAccountFacetBuilder {
            account_login: Vec::new(),
            display_name: None,
            first_login_time: None,
            is_disabled: None,
            last_login_time: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DigitalAccountFacetBuilder {
    account_login: Vec<String>,
    display_name: Option<String>,
    first_login_time: Option<String>,
    is_disabled: Option<bool>,
    last_login_time: Option<String>,
}

impl DigitalAccountFacetBuilder {
    pub fn account_login(mut self, value: Vec<String>) -> Self {
        self.account_login = value;
        self
    }

    pub fn display_name(mut self, value: String) -> Self {
        self.display_name = Some(value);
        self
    }

    pub fn first_login_time(mut self, value: String) -> Self {
        self.first_login_time = Some(value);
        self
    }

    pub fn is_disabled(mut self, value: bool) -> Self {
        self.is_disabled = Some(value);
        self
    }

    pub fn last_login_time(mut self, value: String) -> Self {
        self.last_login_time = Some(value);
        self
    }

    pub fn build(self) -> DigitalAccountFacet {
        DigitalAccountFacet {
            class_iri: DigitalAccountFacet::CLASS_IRI,
            account_login: self.account_login,
            display_name: self.display_name,
            first_login_time: self.first_login_time,
            is_disabled: self.is_disabled,
            last_login_time: self.last_login_time,
        }
    }
}

impl CaseObject for DigitalAccountFacet {
    fn class_iri() -> &'static str { DigitalAccountFacet::CLASS_IRI }
    fn type_name() -> &'static str { "DigitalAccountFacet" }
}

/// A digital address is an identifier assigned to enable routing and management of digital communication.
#[derive(Debug, Clone, Serialize)]
pub struct DigitalAddress {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl DigitalAddress {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalAddress";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DigitalAddressBuilder {
        DigitalAddressBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DigitalAddressBuilder {
}

impl DigitalAddressBuilder {
    pub fn build(self) -> DigitalAddress {
        DigitalAddress {
            class_iri: DigitalAddress::CLASS_IRI,
        }
    }
}

impl CaseObject for DigitalAddress {
    fn class_iri() -> &'static str { DigitalAddress::CLASS_IRI }
    fn type_name() -> &'static str { "DigitalAddress" }
}

/// A digital address facet is a grouping of characteristics unique to an identifier assigned to enable routing and management of digital communication.
#[derive(Debug, Clone, Serialize)]
pub struct DigitalAddressFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:addressValue")]
    pub address_value: Option<String>,
    #[serde(rename = "uco-observable:displayName")]
    pub display_name: Option<String>,
}

impl DigitalAddressFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalAddressFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DigitalAddressFacetBuilder {
        DigitalAddressFacetBuilder {
            address_value: None,
            display_name: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DigitalAddressFacetBuilder {
    address_value: Option<String>,
    display_name: Option<String>,
}

impl DigitalAddressFacetBuilder {
    pub fn address_value(mut self, value: String) -> Self {
        self.address_value = Some(value);
        self
    }

    pub fn display_name(mut self, value: String) -> Self {
        self.display_name = Some(value);
        self
    }

    pub fn build(self) -> DigitalAddressFacet {
        DigitalAddressFacet {
            class_iri: DigitalAddressFacet::CLASS_IRI,
            address_value: self.address_value,
            display_name: self.display_name,
        }
    }
}

impl CaseObject for DigitalAddressFacet {
    fn class_iri() -> &'static str { DigitalAddressFacet::CLASS_IRI }
    fn type_name() -> &'static str { "DigitalAddressFacet" }
}

/// A digital camera is a camera that captures photographs in digital memory as opposed to capturing images on photographic film.
#[derive(Debug, Clone, Serialize)]
pub struct DigitalCamera {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl DigitalCamera {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalCamera";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DigitalCameraBuilder {
        DigitalCameraBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DigitalCameraBuilder {
}

impl DigitalCameraBuilder {
    pub fn build(self) -> DigitalCamera {
        DigitalCamera {
            class_iri: DigitalCamera::CLASS_IRI,
        }
    }
}

impl CaseObject for DigitalCamera {
    fn class_iri() -> &'static str { DigitalCamera::CLASS_IRI }
    fn type_name() -> &'static str { "DigitalCamera" }
}

/// A digital signature info is a value calculated via a mathematical scheme for demonstrating the authenticity of an electronic message or document.
#[derive(Debug, Clone, Serialize)]
pub struct DigitalSignatureInfo {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl DigitalSignatureInfo {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalSignatureInfo";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DigitalSignatureInfoBuilder {
        DigitalSignatureInfoBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DigitalSignatureInfoBuilder {
}

impl DigitalSignatureInfoBuilder {
    pub fn build(self) -> DigitalSignatureInfo {
        DigitalSignatureInfo {
            class_iri: DigitalSignatureInfo::CLASS_IRI,
        }
    }
}

impl CaseObject for DigitalSignatureInfo {
    fn class_iri() -> &'static str { DigitalSignatureInfo::CLASS_IRI }
    fn type_name() -> &'static str { "DigitalSignatureInfo" }
}

/// A digital signature info facet is a grouping of characteristics unique to a value calculated via a mathematical scheme for demonstrating the authenticity of an electronic message or document.
#[derive(Debug, Clone, Serialize)]
pub struct DigitalSignatureInfoFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:certificateIssuer")]
    pub certificate_issuer: Option<Identity>,
    #[serde(rename = "uco-observable:certificateSubject")]
    pub certificate_subject: Option<UcoObject>,
    #[serde(rename = "uco-observable:signatureDescription")]
    pub signature_description: Option<String>,
    #[serde(rename = "uco-observable:signatureExists")]
    pub signature_exists: Option<bool>,
    #[serde(rename = "uco-observable:signatureVerified")]
    pub signature_verified: Option<bool>,
}

impl DigitalSignatureInfoFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DigitalSignatureInfoFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DigitalSignatureInfoFacetBuilder {
        DigitalSignatureInfoFacetBuilder {
            certificate_issuer: None,
            certificate_subject: None,
            signature_description: None,
            signature_exists: None,
            signature_verified: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DigitalSignatureInfoFacetBuilder {
    certificate_issuer: Option<Identity>,
    certificate_subject: Option<UcoObject>,
    signature_description: Option<String>,
    signature_exists: Option<bool>,
    signature_verified: Option<bool>,
}

impl DigitalSignatureInfoFacetBuilder {
    pub fn certificate_issuer(mut self, value: Identity) -> Self {
        self.certificate_issuer = Some(value);
        self
    }

    pub fn certificate_subject(mut self, value: UcoObject) -> Self {
        self.certificate_subject = Some(value);
        self
    }

    pub fn signature_description(mut self, value: String) -> Self {
        self.signature_description = Some(value);
        self
    }

    pub fn signature_exists(mut self, value: bool) -> Self {
        self.signature_exists = Some(value);
        self
    }

    pub fn signature_verified(mut self, value: bool) -> Self {
        self.signature_verified = Some(value);
        self
    }

    pub fn build(self) -> DigitalSignatureInfoFacet {
        DigitalSignatureInfoFacet {
            class_iri: DigitalSignatureInfoFacet::CLASS_IRI,
            certificate_issuer: self.certificate_issuer,
            certificate_subject: self.certificate_subject,
            signature_description: self.signature_description,
            signature_exists: self.signature_exists,
            signature_verified: self.signature_verified,
        }
    }
}

impl CaseObject for DigitalSignatureInfoFacet {
    fn class_iri() -> &'static str { DigitalSignatureInfoFacet::CLASS_IRI }
    fn type_name() -> &'static str { "DigitalSignatureInfoFacet" }
}

/// A directory is a file system cataloging structure which contains references to other computer files, and possibly other directories. On many computers, directories are known as folders, or drawers, an
#[derive(Debug, Clone, Serialize)]
pub struct Directory {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Directory {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Directory";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DirectoryBuilder {
        DirectoryBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DirectoryBuilder {
}

impl DirectoryBuilder {
    pub fn build(self) -> Directory {
        Directory {
            class_iri: Directory::CLASS_IRI,
        }
    }
}

impl CaseObject for Directory {
    fn class_iri() -> &'static str { Directory::CLASS_IRI }
    fn type_name() -> &'static str { "Directory" }
}

/// A disk is a storage mechanism where data is recorded by various electronic, magnetic, optical, or mechanical changes to a surface layer of one or more rotating disks.
#[derive(Debug, Clone, Serialize)]
pub struct Disk {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Disk {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Disk";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DiskBuilder {
        DiskBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DiskBuilder {
}

impl DiskBuilder {
    pub fn build(self) -> Disk {
        Disk {
            class_iri: Disk::CLASS_IRI,
        }
    }
}

impl CaseObject for Disk {
    fn class_iri() -> &'static str { Disk::CLASS_IRI }
    fn type_name() -> &'static str { "Disk" }
}

/// A disk facet is a grouping of characteristics unique to a storage mechanism where data is recorded by various electronic, magnetic, optical, or mechanical changes to a surface layer of one or more rot
#[derive(Debug, Clone, Serialize)]
pub struct DiskFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:diskSize")]
    pub disk_size: Option<i64>,
    #[serde(rename = "uco-observable:diskType")]
    pub disk_type: Option<String>,
    #[serde(rename = "uco-observable:freeSpace")]
    pub free_space: Option<i64>,
    #[serde(rename = "uco-observable:partition")]
    pub partition: Vec<ObservableObject>,
}

impl DiskFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DiskFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DiskFacetBuilder {
        DiskFacetBuilder {
            disk_size: None,
            disk_type: None,
            free_space: None,
            partition: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DiskFacetBuilder {
    disk_size: Option<i64>,
    disk_type: Option<String>,
    free_space: Option<i64>,
    partition: Vec<ObservableObject>,
}

impl DiskFacetBuilder {
    pub fn disk_size(mut self, value: i64) -> Self {
        self.disk_size = Some(value);
        self
    }

    pub fn disk_type(mut self, value: String) -> Self {
        self.disk_type = Some(value);
        self
    }

    pub fn free_space(mut self, value: i64) -> Self {
        self.free_space = Some(value);
        self
    }

    pub fn partition(mut self, value: Vec<ObservableObject>) -> Self {
        self.partition = value;
        self
    }

    pub fn build(self) -> DiskFacet {
        DiskFacet {
            class_iri: DiskFacet::CLASS_IRI,
            disk_size: self.disk_size,
            disk_type: self.disk_type,
            free_space: self.free_space,
            partition: self.partition,
        }
    }
}

impl CaseObject for DiskFacet {
    fn class_iri() -> &'static str { DiskFacet::CLASS_IRI }
    fn type_name() -> &'static str { "DiskFacet" }
}

/// A disk partition is a particular managed region on a storage mechanism where data is recorded by various electronic, magnetic, optical, or mechanical changes to a surface layer of one or more rotating
#[derive(Debug, Clone, Serialize)]
pub struct DiskPartition {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl DiskPartition {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DiskPartition";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DiskPartitionBuilder {
        DiskPartitionBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DiskPartitionBuilder {
}

impl DiskPartitionBuilder {
    pub fn build(self) -> DiskPartition {
        DiskPartition {
            class_iri: DiskPartition::CLASS_IRI,
        }
    }
}

impl CaseObject for DiskPartition {
    fn class_iri() -> &'static str { DiskPartition::CLASS_IRI }
    fn type_name() -> &'static str { "DiskPartition" }
}

/// A disk partition facet is a grouping of characteristics unique to a particular managed region on a storage mechanism.
#[derive(Debug, Clone, Serialize)]
pub struct DiskPartitionFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:diskPartitionType")]
    pub disk_partition_type: Option<String>,
    #[serde(rename = "uco-observable:mountPoint")]
    pub mount_point: Option<String>,
    #[serde(rename = "uco-observable:observableCreatedTime")]
    pub observable_created_time: Option<String>,
    #[serde(rename = "uco-observable:partitionID")]
    pub partition_id: Option<String>,
    #[serde(rename = "uco-observable:partitionLength")]
    pub partition_length: Option<i64>,
    #[serde(rename = "uco-observable:partitionOffset")]
    pub partition_offset: Option<i64>,
    #[serde(rename = "uco-observable:spaceLeft")]
    pub space_left: Option<i64>,
    #[serde(rename = "uco-observable:spaceUsed")]
    pub space_used: Option<i64>,
    #[serde(rename = "uco-observable:totalSpace")]
    pub total_space: Option<i64>,
}

impl DiskPartitionFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DiskPartitionFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DiskPartitionFacetBuilder {
        DiskPartitionFacetBuilder {
            disk_partition_type: None,
            mount_point: None,
            observable_created_time: None,
            partition_id: None,
            partition_length: None,
            partition_offset: None,
            space_left: None,
            space_used: None,
            total_space: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DiskPartitionFacetBuilder {
    disk_partition_type: Option<String>,
    mount_point: Option<String>,
    observable_created_time: Option<String>,
    partition_id: Option<String>,
    partition_length: Option<i64>,
    partition_offset: Option<i64>,
    space_left: Option<i64>,
    space_used: Option<i64>,
    total_space: Option<i64>,
}

impl DiskPartitionFacetBuilder {
    pub fn disk_partition_type(mut self, value: String) -> Self {
        self.disk_partition_type = Some(value);
        self
    }

    pub fn mount_point(mut self, value: String) -> Self {
        self.mount_point = Some(value);
        self
    }

    pub fn observable_created_time(mut self, value: String) -> Self {
        self.observable_created_time = Some(value);
        self
    }

    pub fn partition_id(mut self, value: String) -> Self {
        self.partition_id = Some(value);
        self
    }

    pub fn partition_length(mut self, value: i64) -> Self {
        self.partition_length = Some(value);
        self
    }

    pub fn partition_offset(mut self, value: i64) -> Self {
        self.partition_offset = Some(value);
        self
    }

    pub fn space_left(mut self, value: i64) -> Self {
        self.space_left = Some(value);
        self
    }

    pub fn space_used(mut self, value: i64) -> Self {
        self.space_used = Some(value);
        self
    }

    pub fn total_space(mut self, value: i64) -> Self {
        self.total_space = Some(value);
        self
    }

    pub fn build(self) -> DiskPartitionFacet {
        DiskPartitionFacet {
            class_iri: DiskPartitionFacet::CLASS_IRI,
            disk_partition_type: self.disk_partition_type,
            mount_point: self.mount_point,
            observable_created_time: self.observable_created_time,
            partition_id: self.partition_id,
            partition_length: self.partition_length,
            partition_offset: self.partition_offset,
            space_left: self.space_left,
            space_used: self.space_used,
            total_space: self.total_space,
        }
    }
}

impl CaseObject for DiskPartitionFacet {
    fn class_iri() -> &'static str { DiskPartitionFacet::CLASS_IRI }
    fn type_name() -> &'static str { "DiskPartitionFacet" }
}

/// A domain name is an identification string that defines a realm of administrative autonomy, authority or control within the Internet. [based on https://en.wikipedia.org/wiki/Domain_name]
#[derive(Debug, Clone, Serialize)]
pub struct DomainName {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl DomainName {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DomainName";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DomainNameBuilder {
        DomainNameBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DomainNameBuilder {
}

impl DomainNameBuilder {
    pub fn build(self) -> DomainName {
        DomainName {
            class_iri: DomainName::CLASS_IRI,
        }
    }
}

impl CaseObject for DomainName {
    fn class_iri() -> &'static str { DomainName::CLASS_IRI }
    fn type_name() -> &'static str { "DomainName" }
}

/// A domain name facet is a grouping of characteristics unique to an identification string that defines a realm of administrative autonomy, authority or control within the Internet. [based on https://en.
#[derive(Debug, Clone, Serialize)]
pub struct DomainNameFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:isTLD")]
    pub is_tld: Option<bool>,
    #[serde(rename = "uco-observable:value")]
    pub value: Option<String>,
}

impl DomainNameFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/DomainNameFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DomainNameFacetBuilder {
        DomainNameFacetBuilder {
            is_tld: None,
            value: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DomainNameFacetBuilder {
    is_tld: Option<bool>,
    value: Option<String>,
}

impl DomainNameFacetBuilder {
    pub fn is_tld(mut self, value: bool) -> Self {
        self.is_tld = Some(value);
        self
    }

    pub fn value(mut self, value: String) -> Self {
        self.value = Some(value);
        self
    }

    pub fn build(self) -> DomainNameFacet {
        DomainNameFacet {
            class_iri: DomainNameFacet::CLASS_IRI,
            is_tld: self.is_tld,
            value: self.value,
        }
    }
}

impl CaseObject for DomainNameFacet {
    fn class_iri() -> &'static str { DomainNameFacet::CLASS_IRI }
    fn type_name() -> &'static str { "DomainNameFacet" }
}

/// A drone, unmanned aerial vehicle (UAV), is an aircraft without a human pilot, crew, or passengers that typically involve a ground-based controller and a system for communications with the UAV.
#[derive(Debug, Clone, Serialize)]
pub struct Drone {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Drone {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Drone";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> DroneBuilder {
        DroneBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct DroneBuilder {
}

impl DroneBuilder {
    pub fn build(self) -> Drone {
        Drone {
            class_iri: Drone::CLASS_IRI,
        }
    }
}

impl CaseObject for Drone {
    fn class_iri() -> &'static str { Drone::CLASS_IRI }
    fn type_name() -> &'static str { "Drone" }
}

/// An EXIF (exchangeable image file format) facet is a grouping of characteristics unique to the formats for images, sound, and ancillary tags used by digital cameras (including smartphones), scanners an
#[derive(Debug, Clone, Serialize)]
pub struct EXIFFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:exifData")]
    pub exif_data: Vec<ControlledDictionary>,
}

impl EXIFFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/EXIFFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> EXIFFacetBuilder {
        EXIFFacetBuilder {
            exif_data: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EXIFFacetBuilder {
    exif_data: Vec<ControlledDictionary>,
}

impl EXIFFacetBuilder {
    pub fn exif_data(mut self, value: Vec<ControlledDictionary>) -> Self {
        self.exif_data = value;
        self
    }

    pub fn build(self) -> EXIFFacet {
        EXIFFacet {
            class_iri: EXIFFacet::CLASS_IRI,
            exif_data: self.exif_data,
        }
    }
}

impl CaseObject for EXIFFacet {
    fn class_iri() -> &'static str { EXIFFacet::CLASS_IRI }
    fn type_name() -> &'static str { "EXIFFacet" }
}

/// An email account is an arrangement with an entity to enable and control the provision of electronic mail (email) capabilities or services.
#[derive(Debug, Clone, Serialize)]
pub struct EmailAccount {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl EmailAccount {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/EmailAccount";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> EmailAccountBuilder {
        EmailAccountBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EmailAccountBuilder {
}

impl EmailAccountBuilder {
    pub fn build(self) -> EmailAccount {
        EmailAccount {
            class_iri: EmailAccount::CLASS_IRI,
        }
    }
}

impl CaseObject for EmailAccount {
    fn class_iri() -> &'static str { EmailAccount::CLASS_IRI }
    fn type_name() -> &'static str { "EmailAccount" }
}

/// An email account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of electronic mail (email) capabilities or services.
#[derive(Debug, Clone, Serialize)]
pub struct EmailAccountFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:emailAddress")]
    pub email_address: Option<ObservableObject>,
}

impl EmailAccountFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/EmailAccountFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> EmailAccountFacetBuilder {
        EmailAccountFacetBuilder {
            email_address: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EmailAccountFacetBuilder {
    email_address: Option<ObservableObject>,
}

impl EmailAccountFacetBuilder {
    pub fn email_address(mut self, value: ObservableObject) -> Self {
        self.email_address = Some(value);
        self
    }

    pub fn build(self) -> EmailAccountFacet {
        EmailAccountFacet {
            class_iri: EmailAccountFacet::CLASS_IRI,
            email_address: self.email_address,
        }
    }
}

impl CaseObject for EmailAccountFacet {
    fn class_iri() -> &'static str { EmailAccountFacet::CLASS_IRI }
    fn type_name() -> &'static str { "EmailAccountFacet" }
}

/// An email address is an identifier for an electronic mailbox to which electronic mail messages (conformant to the Simple Mail Transfer Protocol (SMTP)) are sent from and delivered to.
#[derive(Debug, Clone, Serialize)]
pub struct EmailAddress {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl EmailAddress {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/EmailAddress";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> EmailAddressBuilder {
        EmailAddressBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EmailAddressBuilder {
}

impl EmailAddressBuilder {
    pub fn build(self) -> EmailAddress {
        EmailAddress {
            class_iri: EmailAddress::CLASS_IRI,
        }
    }
}

impl CaseObject for EmailAddress {
    fn class_iri() -> &'static str { EmailAddress::CLASS_IRI }
    fn type_name() -> &'static str { "EmailAddress" }
}

/// An email address facet is a grouping of characteristics unique to an identifier for an electronic mailbox to which electronic mail messages (conformant to the Simple Mail Transfer Protocol (SMTP)) are
#[derive(Debug, Clone, Serialize)]
pub struct EmailAddressFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl EmailAddressFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/EmailAddressFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> EmailAddressFacetBuilder {
        EmailAddressFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EmailAddressFacetBuilder {
}

impl EmailAddressFacetBuilder {
    pub fn build(self) -> EmailAddressFacet {
        EmailAddressFacet {
            class_iri: EmailAddressFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for EmailAddressFacet {
    fn class_iri() -> &'static str { EmailAddressFacet::CLASS_IRI }
    fn type_name() -> &'static str { "EmailAddressFacet" }
}

/// An email message is a message that is an instance of an electronic mail correspondence conformant to the internet message format described in RFC 5322 and related RFCs.
#[derive(Debug, Clone, Serialize)]
pub struct EmailMessage {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl EmailMessage {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/EmailMessage";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> EmailMessageBuilder {
        EmailMessageBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EmailMessageBuilder {
}

impl EmailMessageBuilder {
    pub fn build(self) -> EmailMessage {
        EmailMessage {
            class_iri: EmailMessage::CLASS_IRI,
        }
    }
}

impl CaseObject for EmailMessage {
    fn class_iri() -> &'static str { EmailMessage::CLASS_IRI }
    fn type_name() -> &'static str { "EmailMessage" }
}

/// An email message facet is a grouping of characteristics unique to a message that is an instance of an electronic mail correspondence conformant to the internet message format described in RFC 5322 and
#[derive(Debug, Clone, Serialize)]
pub struct EmailMessageFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:application")]
    pub application: Option<ObservableObject>,
    #[serde(rename = "uco-observable:bcc")]
    pub bcc: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:body")]
    pub body: Option<String>,
    #[serde(rename = "uco-observable:bodyMultipart")]
    pub body_multipart: Vec<MimePartType>,
    #[serde(rename = "uco-observable:bodyRaw")]
    pub body_raw: Option<ObservableObject>,
    #[serde(rename = "uco-observable:categories")]
    pub categories: Vec<String>,
    #[serde(rename = "uco-observable:cc")]
    pub cc: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:contentDisposition")]
    pub content_disposition: Option<String>,
    #[serde(rename = "uco-observable:contentType")]
    pub content_type: Option<String>,
    #[serde(rename = "uco-observable:from")]
    pub from: Option<ObservableObject>,
    #[serde(rename = "uco-observable:headerRaw")]
    pub header_raw: Option<ObservableObject>,
    #[serde(rename = "uco-observable:inReplyTo")]
    pub in_reply_to: Option<String>,
    #[serde(rename = "uco-observable:isMimeEncoded")]
    pub is_mime_encoded: Option<bool>,
    #[serde(rename = "uco-observable:isMultipart")]
    pub is_multipart: Option<bool>,
    #[serde(rename = "uco-observable:isRead")]
    pub is_read: Option<bool>,
    #[serde(rename = "uco-observable:labels")]
    pub labels: Vec<String>,
    #[serde(rename = "uco-observable:messageID")]
    pub message_id: Option<String>,
    #[serde(rename = "uco-observable:modifiedTime")]
    pub modified_time: Option<String>,
    #[serde(rename = "uco-observable:otherHeaders")]
    pub other_headers: Option<Dictionary>,
    #[serde(rename = "uco-observable:priority")]
    pub priority: Option<String>,
    #[serde(rename = "uco-observable:receivedLines")]
    pub received_lines: Vec<String>,
    #[serde(rename = "uco-observable:receivedTime")]
    pub received_time: Option<String>,
    #[serde(rename = "uco-observable:references")]
    pub references: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:sender")]
    pub sender: Option<ObservableObject>,
    #[serde(rename = "uco-observable:sentTime")]
    pub sent_time: Option<String>,
    #[serde(rename = "uco-observable:subject")]
    pub subject: Option<String>,
    #[serde(rename = "uco-observable:to")]
    pub to: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:xMailer")]
    pub x_mailer: Option<String>,
    #[serde(rename = "uco-observable:xOriginatingIP")]
    pub x_originating_ip: Option<ObservableObject>,
}

impl EmailMessageFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/EmailMessageFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> EmailMessageFacetBuilder {
        EmailMessageFacetBuilder {
            application: None,
            bcc: Vec::new(),
            body: None,
            body_multipart: Vec::new(),
            body_raw: None,
            categories: Vec::new(),
            cc: Vec::new(),
            content_disposition: None,
            content_type: None,
            from: None,
            header_raw: None,
            in_reply_to: None,
            is_mime_encoded: None,
            is_multipart: None,
            is_read: None,
            labels: Vec::new(),
            message_id: None,
            modified_time: None,
            other_headers: None,
            priority: None,
            received_lines: Vec::new(),
            received_time: None,
            references: Vec::new(),
            sender: None,
            sent_time: None,
            subject: None,
            to: Vec::new(),
            x_mailer: None,
            x_originating_ip: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EmailMessageFacetBuilder {
    application: Option<ObservableObject>,
    bcc: Vec<ObservableObject>,
    body: Option<String>,
    body_multipart: Vec<MimePartType>,
    body_raw: Option<ObservableObject>,
    categories: Vec<String>,
    cc: Vec<ObservableObject>,
    content_disposition: Option<String>,
    content_type: Option<String>,
    from: Option<ObservableObject>,
    header_raw: Option<ObservableObject>,
    in_reply_to: Option<String>,
    is_mime_encoded: Option<bool>,
    is_multipart: Option<bool>,
    is_read: Option<bool>,
    labels: Vec<String>,
    message_id: Option<String>,
    modified_time: Option<String>,
    other_headers: Option<Dictionary>,
    priority: Option<String>,
    received_lines: Vec<String>,
    received_time: Option<String>,
    references: Vec<ObservableObject>,
    sender: Option<ObservableObject>,
    sent_time: Option<String>,
    subject: Option<String>,
    to: Vec<ObservableObject>,
    x_mailer: Option<String>,
    x_originating_ip: Option<ObservableObject>,
}

impl EmailMessageFacetBuilder {
    pub fn application(mut self, value: ObservableObject) -> Self {
        self.application = Some(value);
        self
    }

    pub fn bcc(mut self, value: Vec<ObservableObject>) -> Self {
        self.bcc = value;
        self
    }

    pub fn body(mut self, value: String) -> Self {
        self.body = Some(value);
        self
    }

    pub fn body_multipart(mut self, value: Vec<MimePartType>) -> Self {
        self.body_multipart = value;
        self
    }

    pub fn body_raw(mut self, value: ObservableObject) -> Self {
        self.body_raw = Some(value);
        self
    }

    pub fn categories(mut self, value: Vec<String>) -> Self {
        self.categories = value;
        self
    }

    pub fn cc(mut self, value: Vec<ObservableObject>) -> Self {
        self.cc = value;
        self
    }

    pub fn content_disposition(mut self, value: String) -> Self {
        self.content_disposition = Some(value);
        self
    }

    pub fn content_type(mut self, value: String) -> Self {
        self.content_type = Some(value);
        self
    }

    pub fn from(mut self, value: ObservableObject) -> Self {
        self.from = Some(value);
        self
    }

    pub fn header_raw(mut self, value: ObservableObject) -> Self {
        self.header_raw = Some(value);
        self
    }

    pub fn in_reply_to(mut self, value: String) -> Self {
        self.in_reply_to = Some(value);
        self
    }

    pub fn is_mime_encoded(mut self, value: bool) -> Self {
        self.is_mime_encoded = Some(value);
        self
    }

    pub fn is_multipart(mut self, value: bool) -> Self {
        self.is_multipart = Some(value);
        self
    }

    pub fn is_read(mut self, value: bool) -> Self {
        self.is_read = Some(value);
        self
    }

    pub fn labels(mut self, value: Vec<String>) -> Self {
        self.labels = value;
        self
    }

    pub fn message_id(mut self, value: String) -> Self {
        self.message_id = Some(value);
        self
    }

    pub fn modified_time(mut self, value: String) -> Self {
        self.modified_time = Some(value);
        self
    }

    pub fn other_headers(mut self, value: Dictionary) -> Self {
        self.other_headers = Some(value);
        self
    }

    pub fn priority(mut self, value: String) -> Self {
        self.priority = Some(value);
        self
    }

    pub fn received_lines(mut self, value: Vec<String>) -> Self {
        self.received_lines = value;
        self
    }

    pub fn received_time(mut self, value: String) -> Self {
        self.received_time = Some(value);
        self
    }

    pub fn references(mut self, value: Vec<ObservableObject>) -> Self {
        self.references = value;
        self
    }

    pub fn sender(mut self, value: ObservableObject) -> Self {
        self.sender = Some(value);
        self
    }

    pub fn sent_time(mut self, value: String) -> Self {
        self.sent_time = Some(value);
        self
    }

    pub fn subject(mut self, value: String) -> Self {
        self.subject = Some(value);
        self
    }

    pub fn to(mut self, value: Vec<ObservableObject>) -> Self {
        self.to = value;
        self
    }

    pub fn x_mailer(mut self, value: String) -> Self {
        self.x_mailer = Some(value);
        self
    }

    pub fn x_originating_ip(mut self, value: ObservableObject) -> Self {
        self.x_originating_ip = Some(value);
        self
    }

    pub fn build(self) -> EmailMessageFacet {
        EmailMessageFacet {
            class_iri: EmailMessageFacet::CLASS_IRI,
            application: self.application,
            bcc: self.bcc,
            body: self.body,
            body_multipart: self.body_multipart,
            body_raw: self.body_raw,
            categories: self.categories,
            cc: self.cc,
            content_disposition: self.content_disposition,
            content_type: self.content_type,
            from: self.from,
            header_raw: self.header_raw,
            in_reply_to: self.in_reply_to,
            is_mime_encoded: self.is_mime_encoded,
            is_multipart: self.is_multipart,
            is_read: self.is_read,
            labels: self.labels,
            message_id: self.message_id,
            modified_time: self.modified_time,
            other_headers: self.other_headers,
            priority: self.priority,
            received_lines: self.received_lines,
            received_time: self.received_time,
            references: self.references,
            sender: self.sender,
            sent_time: self.sent_time,
            subject: self.subject,
            to: self.to,
            x_mailer: self.x_mailer,
            x_originating_ip: self.x_originating_ip,
        }
    }
}

impl CaseObject for EmailMessageFacet {
    fn class_iri() -> &'static str { EmailMessageFacet::CLASS_IRI }
    fn type_name() -> &'static str { "EmailMessageFacet" }
}

/// An embedded device is a highly specialized microprocessor device meant for one or very few specific purposes and is usually embedded or included within another object or as part of a larger system. Ex
#[derive(Debug, Clone, Serialize)]
pub struct EmbeddedDevice {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl EmbeddedDevice {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/EmbeddedDevice";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> EmbeddedDeviceBuilder {
        EmbeddedDeviceBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EmbeddedDeviceBuilder {
}

impl EmbeddedDeviceBuilder {
    pub fn build(self) -> EmbeddedDevice {
        EmbeddedDevice {
            class_iri: EmbeddedDevice::CLASS_IRI,
        }
    }
}

impl CaseObject for EmbeddedDevice {
    fn class_iri() -> &'static str { EmbeddedDevice::CLASS_IRI }
    fn type_name() -> &'static str { "EmbeddedDevice" }
}

/// An encoded stream facet is a grouping of characteristics unique to the conversion of a body of data content from one form to another form.
#[derive(Debug, Clone, Serialize)]
pub struct EncodedStreamFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:encodingMethod")]
    pub encoding_method: Option<String>,
}

impl EncodedStreamFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/EncodedStreamFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> EncodedStreamFacetBuilder {
        EncodedStreamFacetBuilder {
            encoding_method: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EncodedStreamFacetBuilder {
    encoding_method: Option<String>,
}

impl EncodedStreamFacetBuilder {
    pub fn encoding_method(mut self, value: String) -> Self {
        self.encoding_method = Some(value);
        self
    }

    pub fn build(self) -> EncodedStreamFacet {
        EncodedStreamFacet {
            class_iri: EncodedStreamFacet::CLASS_IRI,
            encoding_method: self.encoding_method,
        }
    }
}

impl CaseObject for EncodedStreamFacet {
    fn class_iri() -> &'static str { EncodedStreamFacet::CLASS_IRI }
    fn type_name() -> &'static str { "EncodedStreamFacet" }
}

/// An encrypted stream facet is a grouping of characteristics unique to the conversion of a body of data content from one form to another obfuscated form in such a way that reversing the conversion to ob
#[derive(Debug, Clone, Serialize)]
pub struct EncryptedStreamFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:encryptionIV")]
    pub encryption_iv: Vec<String>,
    #[serde(rename = "uco-observable:encryptionKey")]
    pub encryption_key: Vec<String>,
    #[serde(rename = "uco-observable:encryptionMethod")]
    pub encryption_method: Option<String>,
    #[serde(rename = "uco-observable:encryptionMode")]
    pub encryption_mode: Option<String>,
}

impl EncryptedStreamFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/EncryptedStreamFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> EncryptedStreamFacetBuilder {
        EncryptedStreamFacetBuilder {
            encryption_iv: Vec::new(),
            encryption_key: Vec::new(),
            encryption_method: None,
            encryption_mode: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EncryptedStreamFacetBuilder {
    encryption_iv: Vec<String>,
    encryption_key: Vec<String>,
    encryption_method: Option<String>,
    encryption_mode: Option<String>,
}

impl EncryptedStreamFacetBuilder {
    pub fn encryption_iv(mut self, value: Vec<String>) -> Self {
        self.encryption_iv = value;
        self
    }

    pub fn encryption_key(mut self, value: Vec<String>) -> Self {
        self.encryption_key = value;
        self
    }

    pub fn encryption_method(mut self, value: String) -> Self {
        self.encryption_method = Some(value);
        self
    }

    pub fn encryption_mode(mut self, value: String) -> Self {
        self.encryption_mode = Some(value);
        self
    }

    pub fn build(self) -> EncryptedStreamFacet {
        EncryptedStreamFacet {
            class_iri: EncryptedStreamFacet::CLASS_IRI,
            encryption_iv: self.encryption_iv,
            encryption_key: self.encryption_key,
            encryption_method: self.encryption_method,
            encryption_mode: self.encryption_mode,
        }
    }
}

impl CaseObject for EncryptedStreamFacet {
    fn class_iri() -> &'static str { EncryptedStreamFacet::CLASS_IRI }
    fn type_name() -> &'static str { "EncryptedStreamFacet" }
}

/// An environment variable is a grouping of characteristics unique to a dynamic-named value that can affect the way running processes will behave on a computer. [based on https://en.wikipedia.org/wiki/En
#[derive(Debug, Clone, Serialize)]
pub struct EnvironmentVariable {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:name")]
    pub name: Option<String>,
    #[serde(rename = "uco-observable:value")]
    pub value: Option<String>,
}

impl EnvironmentVariable {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/EnvironmentVariable";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> EnvironmentVariableBuilder {
        EnvironmentVariableBuilder {
            name: None,
            value: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EnvironmentVariableBuilder {
    name: Option<String>,
    value: Option<String>,
}

impl EnvironmentVariableBuilder {
    pub fn name(mut self, value: String) -> Self {
        self.name = Some(value);
        self
    }

    pub fn value(mut self, value: String) -> Self {
        self.value = Some(value);
        self
    }

    pub fn build(self) -> EnvironmentVariable {
        EnvironmentVariable {
            class_iri: EnvironmentVariable::CLASS_IRI,
            name: self.name,
            value: self.value,
        }
    }
}

impl CaseObject for EnvironmentVariable {
    fn class_iri() -> &'static str { EnvironmentVariable::CLASS_IRI }
    fn type_name() -> &'static str { "EnvironmentVariable" }
}

/// An event log is a collection of event records.
#[derive(Debug, Clone, Serialize)]
pub struct EventLog {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl EventLog {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/EventLog";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> EventLogBuilder {
        EventLogBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EventLogBuilder {
}

impl EventLogBuilder {
    pub fn build(self) -> EventLog {
        EventLog {
            class_iri: EventLog::CLASS_IRI,
        }
    }
}

impl CaseObject for EventLog {
    fn class_iri() -> &'static str { EventLog::CLASS_IRI }
    fn type_name() -> &'static str { "EventLog" }
}

/// An event record is something that happens in a digital context (e.g., operating system events).
#[derive(Debug, Clone, Serialize)]
pub struct EventRecord {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl EventRecord {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/EventRecord";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> EventRecordBuilder {
        EventRecordBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EventRecordBuilder {
}

impl EventRecordBuilder {
    pub fn build(self) -> EventRecord {
        EventRecord {
            class_iri: EventRecord::CLASS_IRI,
        }
    }
}

impl CaseObject for EventRecord {
    fn class_iri() -> &'static str { EventRecord::CLASS_IRI }
    fn type_name() -> &'static str { "EventRecord" }
}

/// An event record facet is a grouping of characteristics unique to something that happens in a digital context (e.g., operating system events).
#[derive(Debug, Clone, Serialize)]
pub struct EventRecordFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:account")]
    pub account: Option<ObservableObject>,
    #[serde(rename = "uco-observable:application")]
    pub application: Option<ObservableObject>,
    #[serde(rename = "uco-observable:cyberAction")]
    pub cyber_action: Option<ObservableAction>,
    #[serde(rename = "uco-observable:endTime")]
    pub end_time: Option<String>,
    #[serde(rename = "uco-observable:eventID")]
    pub event_id: Option<String>,
    #[serde(rename = "uco-observable:eventRecordDevice")]
    pub event_record_device: Option<ObservableObject>,
    #[serde(rename = "uco-observable:eventRecordID")]
    pub event_record_id: Option<String>,
    #[serde(rename = "uco-observable:eventRecordRaw")]
    pub event_record_raw: Option<String>,
    #[serde(rename = "uco-observable:eventRecordServiceName")]
    pub event_record_service_name: Option<String>,
    #[serde(rename = "uco-observable:eventRecordText")]
    pub event_record_text: Option<String>,
    #[serde(rename = "uco-observable:eventType")]
    pub event_type: Option<String>,
    #[serde(rename = "uco-observable:observableCreatedTime")]
    pub observable_created_time: Option<String>,
    #[serde(rename = "uco-observable:startTime")]
    pub start_time: Option<String>,
}

impl EventRecordFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/EventRecordFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> EventRecordFacetBuilder {
        EventRecordFacetBuilder {
            account: None,
            application: None,
            cyber_action: None,
            end_time: None,
            event_id: None,
            event_record_device: None,
            event_record_id: None,
            event_record_raw: None,
            event_record_service_name: None,
            event_record_text: None,
            event_type: None,
            observable_created_time: None,
            start_time: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct EventRecordFacetBuilder {
    account: Option<ObservableObject>,
    application: Option<ObservableObject>,
    cyber_action: Option<ObservableAction>,
    end_time: Option<String>,
    event_id: Option<String>,
    event_record_device: Option<ObservableObject>,
    event_record_id: Option<String>,
    event_record_raw: Option<String>,
    event_record_service_name: Option<String>,
    event_record_text: Option<String>,
    event_type: Option<String>,
    observable_created_time: Option<String>,
    start_time: Option<String>,
}

impl EventRecordFacetBuilder {
    pub fn account(mut self, value: ObservableObject) -> Self {
        self.account = Some(value);
        self
    }

    pub fn application(mut self, value: ObservableObject) -> Self {
        self.application = Some(value);
        self
    }

    pub fn cyber_action(mut self, value: ObservableAction) -> Self {
        self.cyber_action = Some(value);
        self
    }

    pub fn end_time(mut self, value: String) -> Self {
        self.end_time = Some(value);
        self
    }

    pub fn event_id(mut self, value: String) -> Self {
        self.event_id = Some(value);
        self
    }

    pub fn event_record_device(mut self, value: ObservableObject) -> Self {
        self.event_record_device = Some(value);
        self
    }

    pub fn event_record_id(mut self, value: String) -> Self {
        self.event_record_id = Some(value);
        self
    }

    pub fn event_record_raw(mut self, value: String) -> Self {
        self.event_record_raw = Some(value);
        self
    }

    pub fn event_record_service_name(mut self, value: String) -> Self {
        self.event_record_service_name = Some(value);
        self
    }

    pub fn event_record_text(mut self, value: String) -> Self {
        self.event_record_text = Some(value);
        self
    }

    pub fn event_type(mut self, value: String) -> Self {
        self.event_type = Some(value);
        self
    }

    pub fn observable_created_time(mut self, value: String) -> Self {
        self.observable_created_time = Some(value);
        self
    }

    pub fn start_time(mut self, value: String) -> Self {
        self.start_time = Some(value);
        self
    }

    pub fn build(self) -> EventRecordFacet {
        EventRecordFacet {
            class_iri: EventRecordFacet::CLASS_IRI,
            account: self.account,
            application: self.application,
            cyber_action: self.cyber_action,
            end_time: self.end_time,
            event_id: self.event_id,
            event_record_device: self.event_record_device,
            event_record_id: self.event_record_id,
            event_record_raw: self.event_record_raw,
            event_record_service_name: self.event_record_service_name,
            event_record_text: self.event_record_text,
            event_type: self.event_type,
            observable_created_time: self.observable_created_time,
            start_time: self.start_time,
        }
    }
}

impl CaseObject for EventRecordFacet {
    fn class_iri() -> &'static str { EventRecordFacet::CLASS_IRI }
    fn type_name() -> &'static str { "EventRecordFacet" }
}

/// An extInode facet is a grouping of characteristics unique to a file system object (file, directory, etc.) conformant to the extended file system (EXT or related derivations) specification.
#[derive(Debug, Clone, Serialize)]
pub struct ExtInodeFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:extDeletionTime")]
    pub ext_deletion_time: Option<String>,
    #[serde(rename = "uco-observable:extFileType")]
    pub ext_file_type: Option<i64>,
    #[serde(rename = "uco-observable:extFlags")]
    pub ext_flags: Option<i64>,
    #[serde(rename = "uco-observable:extHardLinkCount")]
    pub ext_hard_link_count: Option<i64>,
    #[serde(rename = "uco-observable:extInodeChangeTime")]
    pub ext_inode_change_time: Option<String>,
    #[serde(rename = "uco-observable:extInodeID")]
    pub ext_inode_id: Option<i64>,
    #[serde(rename = "uco-observable:extPermissions")]
    pub ext_permissions: Option<i64>,
    #[serde(rename = "uco-observable:extSGID")]
    pub ext_sgid: Option<i64>,
    #[serde(rename = "uco-observable:extSUID")]
    pub ext_suid: Option<i64>,
}

impl ExtInodeFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ExtInodeFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ExtInodeFacetBuilder {
        ExtInodeFacetBuilder {
            ext_deletion_time: None,
            ext_file_type: None,
            ext_flags: None,
            ext_hard_link_count: None,
            ext_inode_change_time: None,
            ext_inode_id: None,
            ext_permissions: None,
            ext_sgid: None,
            ext_suid: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ExtInodeFacetBuilder {
    ext_deletion_time: Option<String>,
    ext_file_type: Option<i64>,
    ext_flags: Option<i64>,
    ext_hard_link_count: Option<i64>,
    ext_inode_change_time: Option<String>,
    ext_inode_id: Option<i64>,
    ext_permissions: Option<i64>,
    ext_sgid: Option<i64>,
    ext_suid: Option<i64>,
}

impl ExtInodeFacetBuilder {
    pub fn ext_deletion_time(mut self, value: String) -> Self {
        self.ext_deletion_time = Some(value);
        self
    }

    pub fn ext_file_type(mut self, value: i64) -> Self {
        self.ext_file_type = Some(value);
        self
    }

    pub fn ext_flags(mut self, value: i64) -> Self {
        self.ext_flags = Some(value);
        self
    }

    pub fn ext_hard_link_count(mut self, value: i64) -> Self {
        self.ext_hard_link_count = Some(value);
        self
    }

    pub fn ext_inode_change_time(mut self, value: String) -> Self {
        self.ext_inode_change_time = Some(value);
        self
    }

    pub fn ext_inode_id(mut self, value: i64) -> Self {
        self.ext_inode_id = Some(value);
        self
    }

    pub fn ext_permissions(mut self, value: i64) -> Self {
        self.ext_permissions = Some(value);
        self
    }

    pub fn ext_sgid(mut self, value: i64) -> Self {
        self.ext_sgid = Some(value);
        self
    }

    pub fn ext_suid(mut self, value: i64) -> Self {
        self.ext_suid = Some(value);
        self
    }

    pub fn build(self) -> ExtInodeFacet {
        ExtInodeFacet {
            class_iri: ExtInodeFacet::CLASS_IRI,
            ext_deletion_time: self.ext_deletion_time,
            ext_file_type: self.ext_file_type,
            ext_flags: self.ext_flags,
            ext_hard_link_count: self.ext_hard_link_count,
            ext_inode_change_time: self.ext_inode_change_time,
            ext_inode_id: self.ext_inode_id,
            ext_permissions: self.ext_permissions,
            ext_sgid: self.ext_sgid,
            ext_suid: self.ext_suid,
        }
    }
}

impl CaseObject for ExtInodeFacet {
    fn class_iri() -> &'static str { ExtInodeFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ExtInodeFacet" }
}

/// An extracted string is a grouping of characteristics unique to a series of characters pulled from an observable object.
#[derive(Debug, Clone, Serialize)]
pub struct ExtractedString {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:byteStringValue")]
    pub byte_string_value: Option<Vec<u8>>,
    #[serde(rename = "uco-observable:encoding")]
    pub encoding: Option<String>,
    #[serde(rename = "uco-observable:englishTranslation")]
    pub english_translation: Option<String>,
    #[serde(rename = "uco-observable:language")]
    pub language: Option<String>,
    #[serde(rename = "uco-observable:length")]
    pub length: Option<i64>,
    #[serde(rename = "uco-observable:stringValue")]
    pub string_value: Option<String>,
}

impl ExtractedString {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ExtractedString";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ExtractedStringBuilder {
        ExtractedStringBuilder {
            byte_string_value: None,
            encoding: None,
            english_translation: None,
            language: None,
            length: None,
            string_value: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ExtractedStringBuilder {
    byte_string_value: Option<Vec<u8>>,
    encoding: Option<String>,
    english_translation: Option<String>,
    language: Option<String>,
    length: Option<i64>,
    string_value: Option<String>,
}

impl ExtractedStringBuilder {
    pub fn byte_string_value(mut self, value: Vec<u8>) -> Self {
        self.byte_string_value = Some(value);
        self
    }

    pub fn encoding(mut self, value: String) -> Self {
        self.encoding = Some(value);
        self
    }

    pub fn english_translation(mut self, value: String) -> Self {
        self.english_translation = Some(value);
        self
    }

    pub fn language(mut self, value: String) -> Self {
        self.language = Some(value);
        self
    }

    pub fn length(mut self, value: i64) -> Self {
        self.length = Some(value);
        self
    }

    pub fn string_value(mut self, value: String) -> Self {
        self.string_value = Some(value);
        self
    }

    pub fn build(self) -> ExtractedString {
        ExtractedString {
            class_iri: ExtractedString::CLASS_IRI,
            byte_string_value: self.byte_string_value,
            encoding: self.encoding,
            english_translation: self.english_translation,
            language: self.language,
            length: self.length,
            string_value: self.string_value,
        }
    }
}

impl CaseObject for ExtractedString {
    fn class_iri() -> &'static str { ExtractedString::CLASS_IRI }
    fn type_name() -> &'static str { "ExtractedString" }
}

/// An extracted strings facet is a grouping of characteristics unique to one or more sequences of characters pulled from an observable object.
#[derive(Debug, Clone, Serialize)]
pub struct ExtractedStringsFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:strings")]
    pub strings: Vec<ExtractedString>,
}

impl ExtractedStringsFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ExtractedStringsFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ExtractedStringsFacetBuilder {
        ExtractedStringsFacetBuilder {
            strings: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ExtractedStringsFacetBuilder {
    strings: Vec<ExtractedString>,
}

impl ExtractedStringsFacetBuilder {
    pub fn strings(mut self, value: Vec<ExtractedString>) -> Self {
        self.strings = value;
        self
    }

    pub fn build(self) -> ExtractedStringsFacet {
        ExtractedStringsFacet {
            class_iri: ExtractedStringsFacet::CLASS_IRI,
            strings: self.strings,
        }
    }
}

impl CaseObject for ExtractedStringsFacet {
    fn class_iri() -> &'static str { ExtractedStringsFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ExtractedStringsFacet" }
}

/// A file is a computer resource for recording data discretely on a computer storage device.
#[derive(Debug, Clone, Serialize)]
pub struct File {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl File {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/File";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> FileBuilder {
        FileBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct FileBuilder {
}

impl FileBuilder {
    pub fn build(self) -> File {
        File {
            class_iri: File::CLASS_IRI,
        }
    }
}

impl CaseObject for File {
    fn class_iri() -> &'static str { File::CLASS_IRI }
    fn type_name() -> &'static str { "File" }
}

/// A file facet is a grouping of characteristics unique to the storage of a file (computer resource for recording data discretely in a computer storage device) on a file system (process that manages how 
#[derive(Debug, Clone, Serialize)]
pub struct FileFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:accessedTime")]
    pub accessed_time: Option<String>,
    #[serde(rename = "uco-observable:allocationStatus")]
    pub allocation_status: Option<String>,
    #[serde(rename = "uco-observable:extension")]
    pub extension: Option<String>,
    #[serde(rename = "uco-observable:fileName")]
    pub file_name: Vec<String>,
    #[serde(rename = "uco-observable:filePath")]
    pub file_path: Vec<String>,
    #[serde(rename = "uco-observable:isDirectory")]
    pub is_directory: Vec<bool>,
    #[serde(rename = "uco-observable:metadataChangeTime")]
    pub metadata_change_time: Option<String>,
    #[serde(rename = "uco-observable:modifiedTime")]
    pub modified_time: Option<String>,
    #[serde(rename = "uco-observable:observableCreatedTime")]
    pub observable_created_time: Option<String>,
    #[serde(rename = "uco-observable:sizeInBytes")]
    pub size_in_bytes: Option<i64>,
}

impl FileFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/FileFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> FileFacetBuilder {
        FileFacetBuilder {
            accessed_time: None,
            allocation_status: None,
            extension: None,
            file_name: Vec::new(),
            file_path: Vec::new(),
            is_directory: Vec::new(),
            metadata_change_time: None,
            modified_time: None,
            observable_created_time: None,
            size_in_bytes: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct FileFacetBuilder {
    accessed_time: Option<String>,
    allocation_status: Option<String>,
    extension: Option<String>,
    file_name: Vec<String>,
    file_path: Vec<String>,
    is_directory: Vec<bool>,
    metadata_change_time: Option<String>,
    modified_time: Option<String>,
    observable_created_time: Option<String>,
    size_in_bytes: Option<i64>,
}

impl FileFacetBuilder {
    pub fn accessed_time(mut self, value: String) -> Self {
        self.accessed_time = Some(value);
        self
    }

    pub fn allocation_status(mut self, value: String) -> Self {
        self.allocation_status = Some(value);
        self
    }

    pub fn extension(mut self, value: String) -> Self {
        self.extension = Some(value);
        self
    }

    pub fn file_name(mut self, value: Vec<String>) -> Self {
        self.file_name = value;
        self
    }

    pub fn file_path(mut self, value: Vec<String>) -> Self {
        self.file_path = value;
        self
    }

    pub fn is_directory(mut self, value: Vec<bool>) -> Self {
        self.is_directory = value;
        self
    }

    pub fn metadata_change_time(mut self, value: String) -> Self {
        self.metadata_change_time = Some(value);
        self
    }

    pub fn modified_time(mut self, value: String) -> Self {
        self.modified_time = Some(value);
        self
    }

    pub fn observable_created_time(mut self, value: String) -> Self {
        self.observable_created_time = Some(value);
        self
    }

    pub fn size_in_bytes(mut self, value: i64) -> Self {
        self.size_in_bytes = Some(value);
        self
    }

    pub fn build(self) -> FileFacet {
        FileFacet {
            class_iri: FileFacet::CLASS_IRI,
            accessed_time: self.accessed_time,
            allocation_status: self.allocation_status,
            extension: self.extension,
            file_name: self.file_name,
            file_path: self.file_path,
            is_directory: self.is_directory,
            metadata_change_time: self.metadata_change_time,
            modified_time: self.modified_time,
            observable_created_time: self.observable_created_time,
            size_in_bytes: self.size_in_bytes,
        }
    }
}

impl CaseObject for FileFacet {
    fn class_iri() -> &'static str { FileFacet::CLASS_IRI }
    fn type_name() -> &'static str { "FileFacet" }
}

/// A file permissions facet is a grouping of characteristics unique to the access rights (e.g., view, change, navigate, execute) of a file on a file system.
#[derive(Debug, Clone, Serialize)]
pub struct FilePermissionsFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:owner")]
    pub owner: Option<UcoObject>,
}

impl FilePermissionsFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/FilePermissionsFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> FilePermissionsFacetBuilder {
        FilePermissionsFacetBuilder {
            owner: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct FilePermissionsFacetBuilder {
    owner: Option<UcoObject>,
}

impl FilePermissionsFacetBuilder {
    pub fn owner(mut self, value: UcoObject) -> Self {
        self.owner = Some(value);
        self
    }

    pub fn build(self) -> FilePermissionsFacet {
        FilePermissionsFacet {
            class_iri: FilePermissionsFacet::CLASS_IRI,
            owner: self.owner,
        }
    }
}

impl CaseObject for FilePermissionsFacet {
    fn class_iri() -> &'static str { FilePermissionsFacet::CLASS_IRI }
    fn type_name() -> &'static str { "FilePermissionsFacet" }
}

/// A file system is the process that manages how and where data on a storage medium is stored, accessed and managed. [based on https://www.techopedia.com/definition/5510/file-system]
#[derive(Debug, Clone, Serialize)]
pub struct FileSystem {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl FileSystem {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/FileSystem";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> FileSystemBuilder {
        FileSystemBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct FileSystemBuilder {
}

impl FileSystemBuilder {
    pub fn build(self) -> FileSystem {
        FileSystem {
            class_iri: FileSystem::CLASS_IRI,
        }
    }
}

impl CaseObject for FileSystem {
    fn class_iri() -> &'static str { FileSystem::CLASS_IRI }
    fn type_name() -> &'static str { "FileSystem" }
}

/// A file system facet is a grouping of characteristics unique to the process that manages how and where data on a storage medium is stored, accessed and managed. [based on https://www.techopedia.com/def
#[derive(Debug, Clone, Serialize)]
pub struct FileSystemFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:clusterSize")]
    pub cluster_size: Option<i64>,
    #[serde(rename = "uco-observable:fileSystemType")]
    pub file_system_type: Option<String>,
}

impl FileSystemFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/FileSystemFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> FileSystemFacetBuilder {
        FileSystemFacetBuilder {
            cluster_size: None,
            file_system_type: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct FileSystemFacetBuilder {
    cluster_size: Option<i64>,
    file_system_type: Option<String>,
}

impl FileSystemFacetBuilder {
    pub fn cluster_size(mut self, value: i64) -> Self {
        self.cluster_size = Some(value);
        self
    }

    pub fn file_system_type(mut self, value: String) -> Self {
        self.file_system_type = Some(value);
        self
    }

    pub fn build(self) -> FileSystemFacet {
        FileSystemFacet {
            class_iri: FileSystemFacet::CLASS_IRI,
            cluster_size: self.cluster_size,
            file_system_type: self.file_system_type,
        }
    }
}

impl CaseObject for FileSystemFacet {
    fn class_iri() -> &'static str { FileSystemFacet::CLASS_IRI }
    fn type_name() -> &'static str { "FileSystemFacet" }
}

/// A file system object is an informational object represented and managed within a file system.
#[derive(Debug, Clone, Serialize)]
pub struct FileSystemObject {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl FileSystemObject {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/FileSystemObject";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> FileSystemObjectBuilder {
        FileSystemObjectBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct FileSystemObjectBuilder {
}

impl FileSystemObjectBuilder {
    pub fn build(self) -> FileSystemObject {
        FileSystemObject {
            class_iri: FileSystemObject::CLASS_IRI,
        }
    }
}

impl CaseObject for FileSystemObject {
    fn class_iri() -> &'static str { FileSystemObject::CLASS_IRI }
    fn type_name() -> &'static str { "FileSystemObject" }
}

/// A forum post is message submitted by a user account to an online forum where the message content (and typically metadata including who posted it and when) is viewable by any party with viewing permiss
#[derive(Debug, Clone, Serialize)]
pub struct ForumPost {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ForumPost {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ForumPost";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ForumPostBuilder {
        ForumPostBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ForumPostBuilder {
}

impl ForumPostBuilder {
    pub fn build(self) -> ForumPost {
        ForumPost {
            class_iri: ForumPost::CLASS_IRI,
        }
    }
}

impl CaseObject for ForumPost {
    fn class_iri() -> &'static str { ForumPost::CLASS_IRI }
    fn type_name() -> &'static str { "ForumPost" }
}

/// A forum private message (aka PM or DM (direct message)) is a one-to-one message from one specific user account to another specific user account on an online form where transmission is managed by the o
#[derive(Debug, Clone, Serialize)]
pub struct ForumPrivateMessage {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ForumPrivateMessage {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ForumPrivateMessage";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ForumPrivateMessageBuilder {
        ForumPrivateMessageBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ForumPrivateMessageBuilder {
}

impl ForumPrivateMessageBuilder {
    pub fn build(self) -> ForumPrivateMessage {
        ForumPrivateMessage {
            class_iri: ForumPrivateMessage::CLASS_IRI,
        }
    }
}

impl CaseObject for ForumPrivateMessage {
    fn class_iri() -> &'static str { ForumPrivateMessage::CLASS_IRI }
    fn type_name() -> &'static str { "ForumPrivateMessage" }
}

/// A fragment facet is a grouping of characteristics unique to an individual piece of the content of a file.
#[derive(Debug, Clone, Serialize)]
pub struct FragmentFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:fragmentIndex")]
    pub fragment_index: Vec<i64>,
    #[serde(rename = "uco-observable:totalFragments")]
    pub total_fragments: Vec<i64>,
}

impl FragmentFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/FragmentFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> FragmentFacetBuilder {
        FragmentFacetBuilder {
            fragment_index: Vec::new(),
            total_fragments: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct FragmentFacetBuilder {
    fragment_index: Vec<i64>,
    total_fragments: Vec<i64>,
}

impl FragmentFacetBuilder {
    pub fn fragment_index(mut self, value: Vec<i64>) -> Self {
        self.fragment_index = value;
        self
    }

    pub fn total_fragments(mut self, value: Vec<i64>) -> Self {
        self.total_fragments = value;
        self
    }

    pub fn build(self) -> FragmentFacet {
        FragmentFacet {
            class_iri: FragmentFacet::CLASS_IRI,
            fragment_index: self.fragment_index,
            total_fragments: self.total_fragments,
        }
    }
}

impl CaseObject for FragmentFacet {
    fn class_iri() -> &'static str { FragmentFacet::CLASS_IRI }
    fn type_name() -> &'static str { "FragmentFacet" }
}

/// A GUI is a graphical user interface that allows users to interact with electronic devices through graphical icons and audio indicators such as primary notation, instead of text-based user interfaces, 
#[derive(Debug, Clone, Serialize)]
pub struct GUI {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl GUI {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/GUI";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> GUIBuilder {
        GUIBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct GUIBuilder {
}

impl GUIBuilder {
    pub fn build(self) -> GUI {
        GUI {
            class_iri: GUI::CLASS_IRI,
        }
    }
}

impl CaseObject for GUI {
    fn class_iri() -> &'static str { GUI::CLASS_IRI }
    fn type_name() -> &'static str { "GUI" }
}

/// A gaming console (video game console or game console) is an electronic system that connects to a display, typically a TV or computer monitor, for the primary purpose of playing video games.
#[derive(Debug, Clone, Serialize)]
pub struct GamingConsole {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl GamingConsole {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/GamingConsole";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> GamingConsoleBuilder {
        GamingConsoleBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct GamingConsoleBuilder {
}

impl GamingConsoleBuilder {
    pub fn build(self) -> GamingConsole {
        GamingConsole {
            class_iri: GamingConsole::CLASS_IRI,
        }
    }
}

impl CaseObject for GamingConsole {
    fn class_iri() -> &'static str { GamingConsole::CLASS_IRI }
    fn type_name() -> &'static str { "GamingConsole" }
}

/// A generic observable object is an article or unit within the digital domain.
#[derive(Debug, Clone, Serialize)]
pub struct GenericObservableObject {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl GenericObservableObject {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/GenericObservableObject";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> GenericObservableObjectBuilder {
        GenericObservableObjectBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct GenericObservableObjectBuilder {
}

impl GenericObservableObjectBuilder {
    pub fn build(self) -> GenericObservableObject {
        GenericObservableObject {
            class_iri: GenericObservableObject::CLASS_IRI,
        }
    }
}

impl CaseObject for GenericObservableObject {
    fn class_iri() -> &'static str { GenericObservableObject::CLASS_IRI }
    fn type_name() -> &'static str { "GenericObservableObject" }
}

/// A geolocation entry is a single application-specific geolocation entry.
#[derive(Debug, Clone, Serialize)]
pub struct GeoLocationEntry {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl GeoLocationEntry {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationEntry";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> GeoLocationEntryBuilder {
        GeoLocationEntryBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct GeoLocationEntryBuilder {
}

impl GeoLocationEntryBuilder {
    pub fn build(self) -> GeoLocationEntry {
        GeoLocationEntry {
            class_iri: GeoLocationEntry::CLASS_IRI,
        }
    }
}

impl CaseObject for GeoLocationEntry {
    fn class_iri() -> &'static str { GeoLocationEntry::CLASS_IRI }
    fn type_name() -> &'static str { "GeoLocationEntry" }
}

/// A geolocation entry facet is a grouping of characteristics unique to a single application-specific geolocation entry.
#[derive(Debug, Clone, Serialize)]
pub struct GeoLocationEntryFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:application")]
    pub application: Option<ObservableObject>,
    #[serde(rename = "uco-observable:location")]
    pub location: Option<Location>,
    #[serde(rename = "uco-observable:observableCreatedTime")]
    pub observable_created_time: Option<String>,
}

impl GeoLocationEntryFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationEntryFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> GeoLocationEntryFacetBuilder {
        GeoLocationEntryFacetBuilder {
            application: None,
            location: None,
            observable_created_time: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct GeoLocationEntryFacetBuilder {
    application: Option<ObservableObject>,
    location: Option<Location>,
    observable_created_time: Option<String>,
}

impl GeoLocationEntryFacetBuilder {
    pub fn application(mut self, value: ObservableObject) -> Self {
        self.application = Some(value);
        self
    }

    pub fn location(mut self, value: Location) -> Self {
        self.location = Some(value);
        self
    }

    pub fn observable_created_time(mut self, value: String) -> Self {
        self.observable_created_time = Some(value);
        self
    }

    pub fn build(self) -> GeoLocationEntryFacet {
        GeoLocationEntryFacet {
            class_iri: GeoLocationEntryFacet::CLASS_IRI,
            application: self.application,
            location: self.location,
            observable_created_time: self.observable_created_time,
        }
    }
}

impl CaseObject for GeoLocationEntryFacet {
    fn class_iri() -> &'static str { GeoLocationEntryFacet::CLASS_IRI }
    fn type_name() -> &'static str { "GeoLocationEntryFacet" }
}

/// A geolocation log is a record containing geolocation tracks and/or geolocation entries.
#[derive(Debug, Clone, Serialize)]
pub struct GeoLocationLog {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl GeoLocationLog {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationLog";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> GeoLocationLogBuilder {
        GeoLocationLogBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct GeoLocationLogBuilder {
}

impl GeoLocationLogBuilder {
    pub fn build(self) -> GeoLocationLog {
        GeoLocationLog {
            class_iri: GeoLocationLog::CLASS_IRI,
        }
    }
}

impl CaseObject for GeoLocationLog {
    fn class_iri() -> &'static str { GeoLocationLog::CLASS_IRI }
    fn type_name() -> &'static str { "GeoLocationLog" }
}

/// A geolocation log facet is a grouping of characteristics unique to a record containing geolocation tracks and/or geolocation entries.
#[derive(Debug, Clone, Serialize)]
pub struct GeoLocationLogFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:application")]
    pub application: Option<ObservableObject>,
    #[serde(rename = "uco-observable:observableCreatedTime")]
    pub observable_created_time: Option<String>,
}

impl GeoLocationLogFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationLogFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> GeoLocationLogFacetBuilder {
        GeoLocationLogFacetBuilder {
            application: None,
            observable_created_time: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct GeoLocationLogFacetBuilder {
    application: Option<ObservableObject>,
    observable_created_time: Option<String>,
}

impl GeoLocationLogFacetBuilder {
    pub fn application(mut self, value: ObservableObject) -> Self {
        self.application = Some(value);
        self
    }

    pub fn observable_created_time(mut self, value: String) -> Self {
        self.observable_created_time = Some(value);
        self
    }

    pub fn build(self) -> GeoLocationLogFacet {
        GeoLocationLogFacet {
            class_iri: GeoLocationLogFacet::CLASS_IRI,
            application: self.application,
            observable_created_time: self.observable_created_time,
        }
    }
}

impl CaseObject for GeoLocationLogFacet {
    fn class_iri() -> &'static str { GeoLocationLogFacet::CLASS_IRI }
    fn type_name() -> &'static str { "GeoLocationLogFacet" }
}

/// A geolocation track is a set of contiguous geolocation entries representing a path/track taken.
#[derive(Debug, Clone, Serialize)]
pub struct GeoLocationTrack {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl GeoLocationTrack {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationTrack";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> GeoLocationTrackBuilder {
        GeoLocationTrackBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct GeoLocationTrackBuilder {
}

impl GeoLocationTrackBuilder {
    pub fn build(self) -> GeoLocationTrack {
        GeoLocationTrack {
            class_iri: GeoLocationTrack::CLASS_IRI,
        }
    }
}

impl CaseObject for GeoLocationTrack {
    fn class_iri() -> &'static str { GeoLocationTrack::CLASS_IRI }
    fn type_name() -> &'static str { "GeoLocationTrack" }
}

/// A geolocation track facet is a grouping of characteristics unique to a set of contiguous geolocation entries representing a path/track taken.
#[derive(Debug, Clone, Serialize)]
pub struct GeoLocationTrackFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:application")]
    pub application: Option<ObservableObject>,
    #[serde(rename = "uco-observable:endTime")]
    pub end_time: Option<String>,
    #[serde(rename = "uco-observable:geoLocationEntry")]
    pub geo_location_entry: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:startTime")]
    pub start_time: Option<String>,
}

impl GeoLocationTrackFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/GeoLocationTrackFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> GeoLocationTrackFacetBuilder {
        GeoLocationTrackFacetBuilder {
            application: None,
            end_time: None,
            geo_location_entry: Vec::new(),
            start_time: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct GeoLocationTrackFacetBuilder {
    application: Option<ObservableObject>,
    end_time: Option<String>,
    geo_location_entry: Vec<ObservableObject>,
    start_time: Option<String>,
}

impl GeoLocationTrackFacetBuilder {
    pub fn application(mut self, value: ObservableObject) -> Self {
        self.application = Some(value);
        self
    }

    pub fn end_time(mut self, value: String) -> Self {
        self.end_time = Some(value);
        self
    }

    pub fn geo_location_entry(mut self, value: Vec<ObservableObject>) -> Self {
        self.geo_location_entry = value;
        self
    }

    pub fn start_time(mut self, value: String) -> Self {
        self.start_time = Some(value);
        self
    }

    pub fn build(self) -> GeoLocationTrackFacet {
        GeoLocationTrackFacet {
            class_iri: GeoLocationTrackFacet::CLASS_IRI,
            application: self.application,
            end_time: self.end_time,
            geo_location_entry: self.geo_location_entry,
            start_time: self.start_time,
        }
    }
}

impl CaseObject for GeoLocationTrackFacet {
    fn class_iri() -> &'static str { GeoLocationTrackFacet::CLASS_IRI }
    fn type_name() -> &'static str { "GeoLocationTrackFacet" }
}

/// A global flag type is a grouping of characteristics unique to the Windows systemwide global variable named NtGlobalFlag that enables various internal debugging, tracing, and validation support in the 
#[derive(Debug, Clone, Serialize)]
pub struct GlobalFlagType {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:abbreviation")]
    pub abbreviation: Option<String>,
    #[serde(rename = "uco-observable:destination")]
    pub destination: Option<String>,
    #[serde(rename = "uco-observable:hexadecimalValue")]
    pub hexadecimal_value: Vec<Vec<u8>>,
    #[serde(rename = "uco-observable:symbolicName")]
    pub symbolic_name: Option<String>,
}

impl GlobalFlagType {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/GlobalFlagType";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> GlobalFlagTypeBuilder {
        GlobalFlagTypeBuilder {
            abbreviation: None,
            destination: None,
            hexadecimal_value: Vec::new(),
            symbolic_name: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct GlobalFlagTypeBuilder {
    abbreviation: Option<String>,
    destination: Option<String>,
    hexadecimal_value: Vec<Vec<u8>>,
    symbolic_name: Option<String>,
}

impl GlobalFlagTypeBuilder {
    pub fn abbreviation(mut self, value: String) -> Self {
        self.abbreviation = Some(value);
        self
    }

    pub fn destination(mut self, value: String) -> Self {
        self.destination = Some(value);
        self
    }

    pub fn hexadecimal_value(mut self, value: Vec<Vec<u8>>) -> Self {
        self.hexadecimal_value = value;
        self
    }

    pub fn symbolic_name(mut self, value: String) -> Self {
        self.symbolic_name = Some(value);
        self
    }

    pub fn build(self) -> GlobalFlagType {
        GlobalFlagType {
            class_iri: GlobalFlagType::CLASS_IRI,
            abbreviation: self.abbreviation,
            destination: self.destination,
            hexadecimal_value: self.hexadecimal_value,
            symbolic_name: self.symbolic_name,
        }
    }
}

impl CaseObject for GlobalFlagType {
    fn class_iri() -> &'static str { GlobalFlagType::CLASS_IRI }
    fn type_name() -> &'static str { "GlobalFlagType" }
}

/// An HTTP connection is network connection that is conformant to the Hypertext Transfer Protocol (HTTP) standard.
#[derive(Debug, Clone, Serialize)]
pub struct HTTPConnection {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl HTTPConnection {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/HTTPConnection";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> HTTPConnectionBuilder {
        HTTPConnectionBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct HTTPConnectionBuilder {
}

impl HTTPConnectionBuilder {
    pub fn build(self) -> HTTPConnection {
        HTTPConnection {
            class_iri: HTTPConnection::CLASS_IRI,
        }
    }
}

impl CaseObject for HTTPConnection {
    fn class_iri() -> &'static str { HTTPConnection::CLASS_IRI }
    fn type_name() -> &'static str { "HTTPConnection" }
}

/// An HTTP connection facet is a grouping of characteristics unique to portions of a network connection that are conformant to the Hypertext Transfer Protocol (HTTP) standard.
#[derive(Debug, Clone, Serialize)]
pub struct HTTPConnectionFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:httpMesageBodyLength")]
    pub http_mesage_body_length: Option<i64>,
    #[serde(rename = "uco-observable:httpMessageBodyData")]
    pub http_message_body_data: Option<ObservableObject>,
    #[serde(rename = "uco-observable:httpRequestHeader")]
    pub http_request_header: Option<Dictionary>,
    #[serde(rename = "uco-observable:requestMethod")]
    pub request_method: Option<String>,
    #[serde(rename = "uco-observable:requestValue")]
    pub request_value: Option<String>,
    #[serde(rename = "uco-observable:requestVersion")]
    pub request_version: Option<String>,
}

impl HTTPConnectionFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/HTTPConnectionFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> HTTPConnectionFacetBuilder {
        HTTPConnectionFacetBuilder {
            http_mesage_body_length: None,
            http_message_body_data: None,
            http_request_header: None,
            request_method: None,
            request_value: None,
            request_version: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct HTTPConnectionFacetBuilder {
    http_mesage_body_length: Option<i64>,
    http_message_body_data: Option<ObservableObject>,
    http_request_header: Option<Dictionary>,
    request_method: Option<String>,
    request_value: Option<String>,
    request_version: Option<String>,
}

impl HTTPConnectionFacetBuilder {
    pub fn http_mesage_body_length(mut self, value: i64) -> Self {
        self.http_mesage_body_length = Some(value);
        self
    }

    pub fn http_message_body_data(mut self, value: ObservableObject) -> Self {
        self.http_message_body_data = Some(value);
        self
    }

    pub fn http_request_header(mut self, value: Dictionary) -> Self {
        self.http_request_header = Some(value);
        self
    }

    pub fn request_method(mut self, value: String) -> Self {
        self.request_method = Some(value);
        self
    }

    pub fn request_value(mut self, value: String) -> Self {
        self.request_value = Some(value);
        self
    }

    pub fn request_version(mut self, value: String) -> Self {
        self.request_version = Some(value);
        self
    }

    pub fn build(self) -> HTTPConnectionFacet {
        HTTPConnectionFacet {
            class_iri: HTTPConnectionFacet::CLASS_IRI,
            http_mesage_body_length: self.http_mesage_body_length,
            http_message_body_data: self.http_message_body_data,
            http_request_header: self.http_request_header,
            request_method: self.request_method,
            request_value: self.request_value,
            request_version: self.request_version,
        }
    }
}

impl CaseObject for HTTPConnectionFacet {
    fn class_iri() -> &'static str { HTTPConnectionFacet::CLASS_IRI }
    fn type_name() -> &'static str { "HTTPConnectionFacet" }
}

/// A hostname is a label that is assigned to a device connected to a computer network and that is used to identify the device in various forms of electronic communication, such as the World Wide Web. A h
#[derive(Debug, Clone, Serialize)]
pub struct Hostname {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Hostname {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Hostname";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> HostnameBuilder {
        HostnameBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct HostnameBuilder {
}

impl HostnameBuilder {
    pub fn build(self) -> Hostname {
        Hostname {
            class_iri: Hostname::CLASS_IRI,
        }
    }
}

impl CaseObject for Hostname {
    fn class_iri() -> &'static str { Hostname::CLASS_IRI }
    fn type_name() -> &'static str { "Hostname" }
}

/// An ICMP connection is a network connection that is conformant to the Internet Control Message Protocol (ICMP) standard.
#[derive(Debug, Clone, Serialize)]
pub struct ICMPConnection {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ICMPConnection {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ICMPConnection";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ICMPConnectionBuilder {
        ICMPConnectionBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ICMPConnectionBuilder {
}

impl ICMPConnectionBuilder {
    pub fn build(self) -> ICMPConnection {
        ICMPConnection {
            class_iri: ICMPConnection::CLASS_IRI,
        }
    }
}

impl CaseObject for ICMPConnection {
    fn class_iri() -> &'static str { ICMPConnection::CLASS_IRI }
    fn type_name() -> &'static str { "ICMPConnection" }
}

/// An ICMP connection facet is a grouping of characteristics unique to portions of a network connection that are conformant to the Internet Control Message Protocol (ICMP) standard.
#[derive(Debug, Clone, Serialize)]
pub struct ICMPConnectionFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:icmpCode")]
    pub icmp_code: Vec<Vec<u8>>,
    #[serde(rename = "uco-observable:icmpType")]
    pub icmp_type: Vec<Vec<u8>>,
}

impl ICMPConnectionFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ICMPConnectionFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ICMPConnectionFacetBuilder {
        ICMPConnectionFacetBuilder {
            icmp_code: Vec::new(),
            icmp_type: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ICMPConnectionFacetBuilder {
    icmp_code: Vec<Vec<u8>>,
    icmp_type: Vec<Vec<u8>>,
}

impl ICMPConnectionFacetBuilder {
    pub fn icmp_code(mut self, value: Vec<Vec<u8>>) -> Self {
        self.icmp_code = value;
        self
    }

    pub fn icmp_type(mut self, value: Vec<Vec<u8>>) -> Self {
        self.icmp_type = value;
        self
    }

    pub fn build(self) -> ICMPConnectionFacet {
        ICMPConnectionFacet {
            class_iri: ICMPConnectionFacet::CLASS_IRI,
            icmp_code: self.icmp_code,
            icmp_type: self.icmp_type,
        }
    }
}

impl CaseObject for ICMPConnectionFacet {
    fn class_iri() -> &'static str { ICMPConnectionFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ICMPConnectionFacet" }
}

/// An IComHandler action type is a grouping of characteristics unique to a Windows Task-related action that fires a Windows COM handler (smart code in the client address space that can optimize calls bet
#[derive(Debug, Clone, Serialize)]
pub struct IComHandlerActionType {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:comClassID")]
    pub com_class_id: Option<String>,
    #[serde(rename = "uco-observable:comData")]
    pub com_data: Option<String>,
}

impl IComHandlerActionType {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/IComHandlerActionType";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> IComHandlerActionTypeBuilder {
        IComHandlerActionTypeBuilder {
            com_class_id: None,
            com_data: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct IComHandlerActionTypeBuilder {
    com_class_id: Option<String>,
    com_data: Option<String>,
}

impl IComHandlerActionTypeBuilder {
    pub fn com_class_id(mut self, value: String) -> Self {
        self.com_class_id = Some(value);
        self
    }

    pub fn com_data(mut self, value: String) -> Self {
        self.com_data = Some(value);
        self
    }

    pub fn build(self) -> IComHandlerActionType {
        IComHandlerActionType {
            class_iri: IComHandlerActionType::CLASS_IRI,
            com_class_id: self.com_class_id,
            com_data: self.com_data,
        }
    }
}

impl CaseObject for IComHandlerActionType {
    fn class_iri() -> &'static str { IComHandlerActionType::CLASS_IRI }
    fn type_name() -> &'static str { "IComHandlerActionType" }
}

/// An IExec action type is a grouping of characteristics unique to an action that executes a command-line operation on a Windows operating system. [based on https://docs.microsoft.com/en-us/windows/win32
#[derive(Debug, Clone, Serialize)]
pub struct IExecActionType {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:execArguments")]
    pub exec_arguments: Option<String>,
    #[serde(rename = "uco-observable:execProgramHashes")]
    pub exec_program_hashes: Vec<Hash>,
    #[serde(rename = "uco-observable:execProgramPath")]
    pub exec_program_path: Option<String>,
    #[serde(rename = "uco-observable:execWorkingDirectory")]
    pub exec_working_directory: Option<String>,
}

impl IExecActionType {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/IExecActionType";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> IExecActionTypeBuilder {
        IExecActionTypeBuilder {
            exec_arguments: None,
            exec_program_hashes: Vec::new(),
            exec_program_path: None,
            exec_working_directory: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct IExecActionTypeBuilder {
    exec_arguments: Option<String>,
    exec_program_hashes: Vec<Hash>,
    exec_program_path: Option<String>,
    exec_working_directory: Option<String>,
}

impl IExecActionTypeBuilder {
    pub fn exec_arguments(mut self, value: String) -> Self {
        self.exec_arguments = Some(value);
        self
    }

    pub fn exec_program_hashes(mut self, value: Vec<Hash>) -> Self {
        self.exec_program_hashes = value;
        self
    }

    pub fn exec_program_path(mut self, value: String) -> Self {
        self.exec_program_path = Some(value);
        self
    }

    pub fn exec_working_directory(mut self, value: String) -> Self {
        self.exec_working_directory = Some(value);
        self
    }

    pub fn build(self) -> IExecActionType {
        IExecActionType {
            class_iri: IExecActionType::CLASS_IRI,
            exec_arguments: self.exec_arguments,
            exec_program_hashes: self.exec_program_hashes,
            exec_program_path: self.exec_program_path,
            exec_working_directory: self.exec_working_directory,
        }
    }
}

impl CaseObject for IExecActionType {
    fn class_iri() -> &'static str { IExecActionType::CLASS_IRI }
    fn type_name() -> &'static str { "IExecActionType" }
}

/// An IP address is an Internet Protocol (IP) standards conformant identifier assigned to a device to enable routing and management of IP standards conformant communication to or from that device.
#[derive(Debug, Clone, Serialize)]
pub struct IPAddress {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl IPAddress {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/IPAddress";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> IPAddressBuilder {
        IPAddressBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct IPAddressBuilder {
}

impl IPAddressBuilder {
    pub fn build(self) -> IPAddress {
        IPAddress {
            class_iri: IPAddress::CLASS_IRI,
        }
    }
}

impl CaseObject for IPAddress {
    fn class_iri() -> &'static str { IPAddress::CLASS_IRI }
    fn type_name() -> &'static str { "IPAddress" }
}

/// An IP address facet is a grouping of characteristics unique to an Internet Protocol (IP) standards conformant identifier assigned to a device to enable routing and management of IP standards conforman
#[derive(Debug, Clone, Serialize)]
pub struct IPAddressFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl IPAddressFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/IPAddressFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> IPAddressFacetBuilder {
        IPAddressFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct IPAddressFacetBuilder {
}

impl IPAddressFacetBuilder {
    pub fn build(self) -> IPAddressFacet {
        IPAddressFacet {
            class_iri: IPAddressFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for IPAddressFacet {
    fn class_iri() -> &'static str { IPAddressFacet::CLASS_IRI }
    fn type_name() -> &'static str { "IPAddressFacet" }
}

/// An IP netmask is a 32-bit 'mask' used to divide an IP address into subnets and specify the network's available hosts.
#[derive(Debug, Clone, Serialize)]
pub struct IPNetmask {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl IPNetmask {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/IPNetmask";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> IPNetmaskBuilder {
        IPNetmaskBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct IPNetmaskBuilder {
}

impl IPNetmaskBuilder {
    pub fn build(self) -> IPNetmask {
        IPNetmask {
            class_iri: IPNetmask::CLASS_IRI,
        }
    }
}

impl CaseObject for IPNetmask {
    fn class_iri() -> &'static str { IPNetmask::CLASS_IRI }
    fn type_name() -> &'static str { "IPNetmask" }
}

/// An iPhone is a smart phone that applies the iOS mobile operating system.
#[derive(Debug, Clone, Serialize)]
pub struct IPhone {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl IPhone {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/IPhone";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> IPhoneBuilder {
        IPhoneBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct IPhoneBuilder {
}

impl IPhoneBuilder {
    pub fn build(self) -> IPhone {
        IPhone {
            class_iri: IPhone::CLASS_IRI,
        }
    }
}

impl CaseObject for IPhone {
    fn class_iri() -> &'static str { IPhone::CLASS_IRI }
    fn type_name() -> &'static str { "IPhone" }
}

/// An IPv4 (Internet Protocol version 4) address is an IPv4 standards conformant identifier assigned to a device to enable routing and management of IPv4 standards conformant communication to or from tha
#[derive(Debug, Clone, Serialize)]
pub struct IPv4Address {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl IPv4Address {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/IPv4Address";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> IPv4AddressBuilder {
        IPv4AddressBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct IPv4AddressBuilder {
}

impl IPv4AddressBuilder {
    pub fn build(self) -> IPv4Address {
        IPv4Address {
            class_iri: IPv4Address::CLASS_IRI,
        }
    }
}

impl CaseObject for IPv4Address {
    fn class_iri() -> &'static str { IPv4Address::CLASS_IRI }
    fn type_name() -> &'static str { "IPv4Address" }
}

/// An IPv4 (Internet Protocol version 4) address facet is a grouping of characteristics unique to an IPv4 standards conformant identifier assigned to a device to enable routing and management of IPv4 sta
#[derive(Debug, Clone, Serialize)]
pub struct IPv4AddressFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl IPv4AddressFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/IPv4AddressFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> IPv4AddressFacetBuilder {
        IPv4AddressFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct IPv4AddressFacetBuilder {
}

impl IPv4AddressFacetBuilder {
    pub fn build(self) -> IPv4AddressFacet {
        IPv4AddressFacet {
            class_iri: IPv4AddressFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for IPv4AddressFacet {
    fn class_iri() -> &'static str { IPv4AddressFacet::CLASS_IRI }
    fn type_name() -> &'static str { "IPv4AddressFacet" }
}

/// An IPv6 (Internet Protocol version 6) address is an IPv6 standards conformant identifier assigned to a device to enable routing and management of IPv6 standards conformant communication to or from tha
#[derive(Debug, Clone, Serialize)]
pub struct IPv6Address {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl IPv6Address {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/IPv6Address";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> IPv6AddressBuilder {
        IPv6AddressBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct IPv6AddressBuilder {
}

impl IPv6AddressBuilder {
    pub fn build(self) -> IPv6Address {
        IPv6Address {
            class_iri: IPv6Address::CLASS_IRI,
        }
    }
}

impl CaseObject for IPv6Address {
    fn class_iri() -> &'static str { IPv6Address::CLASS_IRI }
    fn type_name() -> &'static str { "IPv6Address" }
}

/// An IPv6 (Internet Protocol version 6) address facet is a grouping of characteristics unique to an IPv6 standards conformant identifier assigned to a device to enable routing and management of IPv6 sta
#[derive(Debug, Clone, Serialize)]
pub struct IPv6AddressFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl IPv6AddressFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/IPv6AddressFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> IPv6AddressFacetBuilder {
        IPv6AddressFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct IPv6AddressFacetBuilder {
}

impl IPv6AddressFacetBuilder {
    pub fn build(self) -> IPv6AddressFacet {
        IPv6AddressFacet {
            class_iri: IPv6AddressFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for IPv6AddressFacet {
    fn class_iri() -> &'static str { IPv6AddressFacet::CLASS_IRI }
    fn type_name() -> &'static str { "IPv6AddressFacet" }
}

/// An IShow message action type is a grouping of characteristics unique to an action that shows a message box when a task is activate. [based on https://docs.microsoft.com/en-us/windows/win32/api/tasksch
#[derive(Debug, Clone, Serialize)]
pub struct IShowMessageActionType {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:showMessageBody")]
    pub show_message_body: Option<String>,
    #[serde(rename = "uco-observable:showMessageTitle")]
    pub show_message_title: Option<String>,
}

impl IShowMessageActionType {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/IShowMessageActionType";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> IShowMessageActionTypeBuilder {
        IShowMessageActionTypeBuilder {
            show_message_body: None,
            show_message_title: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct IShowMessageActionTypeBuilder {
    show_message_body: Option<String>,
    show_message_title: Option<String>,
}

impl IShowMessageActionTypeBuilder {
    pub fn show_message_body(mut self, value: String) -> Self {
        self.show_message_body = Some(value);
        self
    }

    pub fn show_message_title(mut self, value: String) -> Self {
        self.show_message_title = Some(value);
        self
    }

    pub fn build(self) -> IShowMessageActionType {
        IShowMessageActionType {
            class_iri: IShowMessageActionType::CLASS_IRI,
            show_message_body: self.show_message_body,
            show_message_title: self.show_message_title,
        }
    }
}

impl CaseObject for IShowMessageActionType {
    fn class_iri() -> &'static str { IShowMessageActionType::CLASS_IRI }
    fn type_name() -> &'static str { "IShowMessageActionType" }
}

/// An image is a complete copy of a hard disk, memory, or other digital media.
#[derive(Debug, Clone, Serialize)]
pub struct Image {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Image {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Image";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ImageBuilder {
        ImageBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ImageBuilder {
}

impl ImageBuilder {
    pub fn build(self) -> Image {
        Image {
            class_iri: Image::CLASS_IRI,
        }
    }
}

impl CaseObject for Image {
    fn class_iri() -> &'static str { Image::CLASS_IRI }
    fn type_name() -> &'static str { "Image" }
}

/// An image facet is a grouping of characteristics unique to a complete copy of a hard disk, memory, or other digital media.
#[derive(Debug, Clone, Serialize)]
pub struct ImageFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:imageType")]
    pub image_type: Option<String>,
}

impl ImageFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ImageFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ImageFacetBuilder {
        ImageFacetBuilder {
            image_type: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ImageFacetBuilder {
    image_type: Option<String>,
}

impl ImageFacetBuilder {
    pub fn image_type(mut self, value: String) -> Self {
        self.image_type = Some(value);
        self
    }

    pub fn build(self) -> ImageFacet {
        ImageFacet {
            class_iri: ImageFacet::CLASS_IRI,
            image_type: self.image_type,
        }
    }
}

impl CaseObject for ImageFacet {
    fn class_iri() -> &'static str { ImageFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ImageFacet" }
}

/// InstantMessagingAddress
#[derive(Debug, Clone, Serialize)]
pub struct InstantMessagingAddress {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl InstantMessagingAddress {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/InstantMessagingAddress";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> InstantMessagingAddressBuilder {
        InstantMessagingAddressBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct InstantMessagingAddressBuilder {
}

impl InstantMessagingAddressBuilder {
    pub fn build(self) -> InstantMessagingAddress {
        InstantMessagingAddress {
            class_iri: InstantMessagingAddress::CLASS_IRI,
        }
    }
}

impl CaseObject for InstantMessagingAddress {
    fn class_iri() -> &'static str { InstantMessagingAddress::CLASS_IRI }
    fn type_name() -> &'static str { "InstantMessagingAddress" }
}

/// An instant messaging address facet is a grouping of characteristics unique to an identifier assigned to enable routing and management of instant messaging digital communication.
#[derive(Debug, Clone, Serialize)]
pub struct InstantMessagingAddressFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl InstantMessagingAddressFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/InstantMessagingAddressFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> InstantMessagingAddressFacetBuilder {
        InstantMessagingAddressFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct InstantMessagingAddressFacetBuilder {
}

impl InstantMessagingAddressFacetBuilder {
    pub fn build(self) -> InstantMessagingAddressFacet {
        InstantMessagingAddressFacet {
            class_iri: InstantMessagingAddressFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for InstantMessagingAddressFacet {
    fn class_iri() -> &'static str { InstantMessagingAddressFacet::CLASS_IRI }
    fn type_name() -> &'static str { "InstantMessagingAddressFacet" }
}

/// A junction is a specific NTFS (New Technology File System) reparse point to redirect a directory access to another directory which can be on the same volume or another volume. A junction is similar to
#[derive(Debug, Clone, Serialize)]
pub struct Junction {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Junction {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Junction";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> JunctionBuilder {
        JunctionBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct JunctionBuilder {
}

impl JunctionBuilder {
    pub fn build(self) -> Junction {
        Junction {
            class_iri: Junction::CLASS_IRI,
        }
    }
}

impl CaseObject for Junction {
    fn class_iri() -> &'static str { Junction::CLASS_IRI }
    fn type_name() -> &'static str { "Junction" }
}

/// A laptop, laptop computer, or notebook computer is a small, portable personal computer with a screen and alphanumeric keyboard. These typically have a clam shell form factor with the screen mounted on
#[derive(Debug, Clone, Serialize)]
pub struct Laptop {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Laptop {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Laptop";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> LaptopBuilder {
        LaptopBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct LaptopBuilder {
}

impl LaptopBuilder {
    pub fn build(self) -> Laptop {
        Laptop {
            class_iri: Laptop::CLASS_IRI,
        }
    }
}

impl CaseObject for Laptop {
    fn class_iri() -> &'static str { Laptop::CLASS_IRI }
    fn type_name() -> &'static str { "Laptop" }
}

/// A library is a suite of data and programming code that is used to develop software programs and applications. [based on https://www.techopedia.com/definition/3828/software-library]
#[derive(Debug, Clone, Serialize)]
pub struct Library {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Library {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Library";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> LibraryBuilder {
        LibraryBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct LibraryBuilder {
}

impl LibraryBuilder {
    pub fn build(self) -> Library {
        Library {
            class_iri: Library::CLASS_IRI,
        }
    }
}

impl CaseObject for Library {
    fn class_iri() -> &'static str { Library::CLASS_IRI }
    fn type_name() -> &'static str { "Library" }
}

/// A library facet is a grouping of characteristics unique to a suite of data and programming code that is used to develop software programs and applications. [based on https://www.techopedia.com/definit
#[derive(Debug, Clone, Serialize)]
pub struct LibraryFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:libraryType")]
    pub library_type: Option<String>,
}

impl LibraryFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/LibraryFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> LibraryFacetBuilder {
        LibraryFacetBuilder {
            library_type: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct LibraryFacetBuilder {
    library_type: Option<String>,
}

impl LibraryFacetBuilder {
    pub fn library_type(mut self, value: String) -> Self {
        self.library_type = Some(value);
        self
    }

    pub fn build(self) -> LibraryFacet {
        LibraryFacet {
            class_iri: LibraryFacet::CLASS_IRI,
            library_type: self.library_type,
        }
    }
}

impl CaseObject for LibraryFacet {
    fn class_iri() -> &'static str { LibraryFacet::CLASS_IRI }
    fn type_name() -> &'static str { "LibraryFacet" }
}

/// A MAC address is a media access control standards conformant identifier assigned to a network interface to enable routing and management of communications at the data link layer of a network segment.
#[derive(Debug, Clone, Serialize)]
pub struct MACAddress {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl MACAddress {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/MACAddress";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MACAddressBuilder {
        MACAddressBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MACAddressBuilder {
}

impl MACAddressBuilder {
    pub fn build(self) -> MACAddress {
        MACAddress {
            class_iri: MACAddress::CLASS_IRI,
        }
    }
}

impl CaseObject for MACAddress {
    fn class_iri() -> &'static str { MACAddress::CLASS_IRI }
    fn type_name() -> &'static str { "MACAddress" }
}

/// A MAC address facet is a grouping of characteristics unique to a media access control standards conformant identifier assigned to a network interface to enable routing and management of communications
#[derive(Debug, Clone, Serialize)]
pub struct MACAddressFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl MACAddressFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/MACAddressFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MACAddressFacetBuilder {
        MACAddressFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MACAddressFacetBuilder {
}

impl MACAddressFacetBuilder {
    pub fn build(self) -> MACAddressFacet {
        MACAddressFacet {
            class_iri: MACAddressFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for MACAddressFacet {
    fn class_iri() -> &'static str { MACAddressFacet::CLASS_IRI }
    fn type_name() -> &'static str { "MACAddressFacet" }
}

/// Memory is a particular region of temporary information storage (e.g., RAM (random access memory), ROM (read only memory)) on a digital device.
#[derive(Debug, Clone, Serialize)]
pub struct Memory {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Memory {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Memory";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MemoryBuilder {
        MemoryBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MemoryBuilder {
}

impl MemoryBuilder {
    pub fn build(self) -> Memory {
        Memory {
            class_iri: Memory::CLASS_IRI,
        }
    }
}

impl CaseObject for Memory {
    fn class_iri() -> &'static str { Memory::CLASS_IRI }
    fn type_name() -> &'static str { "Memory" }
}

/// A memory facet is a grouping of characteristics unique to a particular region of temporary information storage (e.g., RAM (random access memory), ROM (read only memory)) on a digital device.
#[derive(Debug, Clone, Serialize)]
pub struct MemoryFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:blockType")]
    pub block_type: Vec<String>,
    #[serde(rename = "uco-observable:isInjected")]
    pub is_injected: Option<bool>,
    #[serde(rename = "uco-observable:isMapped")]
    pub is_mapped: Option<bool>,
    #[serde(rename = "uco-observable:isProtected")]
    pub is_protected: Option<bool>,
    #[serde(rename = "uco-observable:isVolatile")]
    pub is_volatile: Option<bool>,
    #[serde(rename = "uco-observable:regionEndAddress")]
    pub region_end_address: Vec<Vec<u8>>,
    #[serde(rename = "uco-observable:regionSize")]
    pub region_size: Option<i64>,
    #[serde(rename = "uco-observable:regionStartAddress")]
    pub region_start_address: Vec<Vec<u8>>,
}

impl MemoryFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/MemoryFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MemoryFacetBuilder {
        MemoryFacetBuilder {
            block_type: Vec::new(),
            is_injected: None,
            is_mapped: None,
            is_protected: None,
            is_volatile: None,
            region_end_address: Vec::new(),
            region_size: None,
            region_start_address: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MemoryFacetBuilder {
    block_type: Vec<String>,
    is_injected: Option<bool>,
    is_mapped: Option<bool>,
    is_protected: Option<bool>,
    is_volatile: Option<bool>,
    region_end_address: Vec<Vec<u8>>,
    region_size: Option<i64>,
    region_start_address: Vec<Vec<u8>>,
}

impl MemoryFacetBuilder {
    pub fn block_type(mut self, value: Vec<String>) -> Self {
        self.block_type = value;
        self
    }

    pub fn is_injected(mut self, value: bool) -> Self {
        self.is_injected = Some(value);
        self
    }

    pub fn is_mapped(mut self, value: bool) -> Self {
        self.is_mapped = Some(value);
        self
    }

    pub fn is_protected(mut self, value: bool) -> Self {
        self.is_protected = Some(value);
        self
    }

    pub fn is_volatile(mut self, value: bool) -> Self {
        self.is_volatile = Some(value);
        self
    }

    pub fn region_end_address(mut self, value: Vec<Vec<u8>>) -> Self {
        self.region_end_address = value;
        self
    }

    pub fn region_size(mut self, value: i64) -> Self {
        self.region_size = Some(value);
        self
    }

    pub fn region_start_address(mut self, value: Vec<Vec<u8>>) -> Self {
        self.region_start_address = value;
        self
    }

    pub fn build(self) -> MemoryFacet {
        MemoryFacet {
            class_iri: MemoryFacet::CLASS_IRI,
            block_type: self.block_type,
            is_injected: self.is_injected,
            is_mapped: self.is_mapped,
            is_protected: self.is_protected,
            is_volatile: self.is_volatile,
            region_end_address: self.region_end_address,
            region_size: self.region_size,
            region_start_address: self.region_start_address,
        }
    }
}

impl CaseObject for MemoryFacet {
    fn class_iri() -> &'static str { MemoryFacet::CLASS_IRI }
    fn type_name() -> &'static str { "MemoryFacet" }
}

/// A message is a discrete unit of electronic communication intended by the source for consumption by some recipient or group of recipients. [based on https://en.wikipedia.org/wiki/Message]
#[derive(Debug, Clone, Serialize)]
pub struct Message {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Message {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Message";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MessageBuilder {
        MessageBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MessageBuilder {
}

impl MessageBuilder {
    pub fn build(self) -> Message {
        Message {
            class_iri: Message::CLASS_IRI,
        }
    }
}

impl CaseObject for Message {
    fn class_iri() -> &'static str { Message::CLASS_IRI }
    fn type_name() -> &'static str { "Message" }
}

/// A message facet is a grouping of characteristics unique to a discrete unit of electronic communication intended by the source for consumption by some recipient or group of recipients. [based on https:
#[derive(Debug, Clone, Serialize)]
pub struct MessageFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:application")]
    pub application: Option<ObservableObject>,
    #[serde(rename = "uco-observable:from")]
    pub from: Option<ObservableObject>,
    #[serde(rename = "uco-observable:messageID")]
    pub message_id: Option<String>,
    #[serde(rename = "uco-observable:messageText")]
    pub message_text: Option<String>,
    #[serde(rename = "uco-observable:messageType")]
    pub message_type: Option<String>,
    #[serde(rename = "uco-observable:sentTime")]
    pub sent_time: Option<String>,
    #[serde(rename = "uco-observable:sessionID")]
    pub session_id: Option<String>,
    #[serde(rename = "uco-observable:to")]
    pub to: Vec<ObservableObject>,
}

impl MessageFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/MessageFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MessageFacetBuilder {
        MessageFacetBuilder {
            application: None,
            from: None,
            message_id: None,
            message_text: None,
            message_type: None,
            sent_time: None,
            session_id: None,
            to: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MessageFacetBuilder {
    application: Option<ObservableObject>,
    from: Option<ObservableObject>,
    message_id: Option<String>,
    message_text: Option<String>,
    message_type: Option<String>,
    sent_time: Option<String>,
    session_id: Option<String>,
    to: Vec<ObservableObject>,
}

impl MessageFacetBuilder {
    pub fn application(mut self, value: ObservableObject) -> Self {
        self.application = Some(value);
        self
    }

    pub fn from(mut self, value: ObservableObject) -> Self {
        self.from = Some(value);
        self
    }

    pub fn message_id(mut self, value: String) -> Self {
        self.message_id = Some(value);
        self
    }

    pub fn message_text(mut self, value: String) -> Self {
        self.message_text = Some(value);
        self
    }

    pub fn message_type(mut self, value: String) -> Self {
        self.message_type = Some(value);
        self
    }

    pub fn sent_time(mut self, value: String) -> Self {
        self.sent_time = Some(value);
        self
    }

    pub fn session_id(mut self, value: String) -> Self {
        self.session_id = Some(value);
        self
    }

    pub fn to(mut self, value: Vec<ObservableObject>) -> Self {
        self.to = value;
        self
    }

    pub fn build(self) -> MessageFacet {
        MessageFacet {
            class_iri: MessageFacet::CLASS_IRI,
            application: self.application,
            from: self.from,
            message_id: self.message_id,
            message_text: self.message_text,
            message_type: self.message_type,
            sent_time: self.sent_time,
            session_id: self.session_id,
            to: self.to,
        }
    }
}

impl CaseObject for MessageFacet {
    fn class_iri() -> &'static str { MessageFacet::CLASS_IRI }
    fn type_name() -> &'static str { "MessageFacet" }
}

/// A message thread is a running commentary of electronic messages pertaining to one topic or question.
#[derive(Debug, Clone, Serialize)]
pub struct MessageThread {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl MessageThread {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/MessageThread";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MessageThreadBuilder {
        MessageThreadBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MessageThreadBuilder {
}

impl MessageThreadBuilder {
    pub fn build(self) -> MessageThread {
        MessageThread {
            class_iri: MessageThread::CLASS_IRI,
        }
    }
}

impl CaseObject for MessageThread {
    fn class_iri() -> &'static str { MessageThread::CLASS_IRI }
    fn type_name() -> &'static str { "MessageThread" }
}

/// A message thread facet is a grouping of characteristics unique to a running commentary of electronic messages pertaining to one topic or question.
#[derive(Debug, Clone, Serialize)]
pub struct MessageThreadFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:messageThread")]
    pub message_thread: Option<Thread>,
    #[serde(rename = "uco-observable:participant")]
    pub participant: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:visibility")]
    pub visibility: Option<bool>,
}

impl MessageThreadFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/MessageThreadFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MessageThreadFacetBuilder {
        MessageThreadFacetBuilder {
            message_thread: None,
            participant: Vec::new(),
            visibility: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MessageThreadFacetBuilder {
    message_thread: Option<Thread>,
    participant: Vec<ObservableObject>,
    visibility: Option<bool>,
}

impl MessageThreadFacetBuilder {
    pub fn message_thread(mut self, value: Thread) -> Self {
        self.message_thread = Some(value);
        self
    }

    pub fn participant(mut self, value: Vec<ObservableObject>) -> Self {
        self.participant = value;
        self
    }

    pub fn visibility(mut self, value: bool) -> Self {
        self.visibility = Some(value);
        self
    }

    pub fn build(self) -> MessageThreadFacet {
        MessageThreadFacet {
            class_iri: MessageThreadFacet::CLASS_IRI,
            message_thread: self.message_thread,
            participant: self.participant,
            visibility: self.visibility,
        }
    }
}

impl CaseObject for MessageThreadFacet {
    fn class_iri() -> &'static str { MessageThreadFacet::CLASS_IRI }
    fn type_name() -> &'static str { "MessageThreadFacet" }
}

/// An MFT record facet is a grouping of characteristics unique to the details of a single file as managed in an NTFS (new technology filesystem) master file table (which is a collection of information ab
#[derive(Debug, Clone, Serialize)]
pub struct MftRecordFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:mftFileID")]
    pub mft_file_id: Option<i64>,
    #[serde(rename = "uco-observable:mftFileNameAccessedTime")]
    pub mft_file_name_accessed_time: Option<String>,
    #[serde(rename = "uco-observable:mftFileNameCreatedTime")]
    pub mft_file_name_created_time: Option<String>,
    #[serde(rename = "uco-observable:mftFileNameLength")]
    pub mft_file_name_length: Option<i64>,
    #[serde(rename = "uco-observable:mftFileNameModifiedTime")]
    pub mft_file_name_modified_time: Option<String>,
    #[serde(rename = "uco-observable:mftFileNameRecordChangeTime")]
    pub mft_file_name_record_change_time: Option<String>,
    #[serde(rename = "uco-observable:mftFlags")]
    pub mft_flags: Option<i64>,
    #[serde(rename = "uco-observable:mftParentID")]
    pub mft_parent_id: Option<i64>,
    #[serde(rename = "uco-observable:mftRecordChangeTime")]
    pub mft_record_change_time: Option<String>,
    #[serde(rename = "uco-observable:ntfsHardLinkCount")]
    pub ntfs_hard_link_count: Option<i64>,
    #[serde(rename = "uco-observable:ntfsOwnerID")]
    pub ntfs_owner_id: Option<String>,
    #[serde(rename = "uco-observable:ntfsOwnerSID")]
    pub ntfs_owner_sid: Option<String>,
}

impl MftRecordFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/MftRecordFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MftRecordFacetBuilder {
        MftRecordFacetBuilder {
            mft_file_id: None,
            mft_file_name_accessed_time: None,
            mft_file_name_created_time: None,
            mft_file_name_length: None,
            mft_file_name_modified_time: None,
            mft_file_name_record_change_time: None,
            mft_flags: None,
            mft_parent_id: None,
            mft_record_change_time: None,
            ntfs_hard_link_count: None,
            ntfs_owner_id: None,
            ntfs_owner_sid: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MftRecordFacetBuilder {
    mft_file_id: Option<i64>,
    mft_file_name_accessed_time: Option<String>,
    mft_file_name_created_time: Option<String>,
    mft_file_name_length: Option<i64>,
    mft_file_name_modified_time: Option<String>,
    mft_file_name_record_change_time: Option<String>,
    mft_flags: Option<i64>,
    mft_parent_id: Option<i64>,
    mft_record_change_time: Option<String>,
    ntfs_hard_link_count: Option<i64>,
    ntfs_owner_id: Option<String>,
    ntfs_owner_sid: Option<String>,
}

impl MftRecordFacetBuilder {
    pub fn mft_file_id(mut self, value: i64) -> Self {
        self.mft_file_id = Some(value);
        self
    }

    pub fn mft_file_name_accessed_time(mut self, value: String) -> Self {
        self.mft_file_name_accessed_time = Some(value);
        self
    }

    pub fn mft_file_name_created_time(mut self, value: String) -> Self {
        self.mft_file_name_created_time = Some(value);
        self
    }

    pub fn mft_file_name_length(mut self, value: i64) -> Self {
        self.mft_file_name_length = Some(value);
        self
    }

    pub fn mft_file_name_modified_time(mut self, value: String) -> Self {
        self.mft_file_name_modified_time = Some(value);
        self
    }

    pub fn mft_file_name_record_change_time(mut self, value: String) -> Self {
        self.mft_file_name_record_change_time = Some(value);
        self
    }

    pub fn mft_flags(mut self, value: i64) -> Self {
        self.mft_flags = Some(value);
        self
    }

    pub fn mft_parent_id(mut self, value: i64) -> Self {
        self.mft_parent_id = Some(value);
        self
    }

    pub fn mft_record_change_time(mut self, value: String) -> Self {
        self.mft_record_change_time = Some(value);
        self
    }

    pub fn ntfs_hard_link_count(mut self, value: i64) -> Self {
        self.ntfs_hard_link_count = Some(value);
        self
    }

    pub fn ntfs_owner_id(mut self, value: String) -> Self {
        self.ntfs_owner_id = Some(value);
        self
    }

    pub fn ntfs_owner_sid(mut self, value: String) -> Self {
        self.ntfs_owner_sid = Some(value);
        self
    }

    pub fn build(self) -> MftRecordFacet {
        MftRecordFacet {
            class_iri: MftRecordFacet::CLASS_IRI,
            mft_file_id: self.mft_file_id,
            mft_file_name_accessed_time: self.mft_file_name_accessed_time,
            mft_file_name_created_time: self.mft_file_name_created_time,
            mft_file_name_length: self.mft_file_name_length,
            mft_file_name_modified_time: self.mft_file_name_modified_time,
            mft_file_name_record_change_time: self.mft_file_name_record_change_time,
            mft_flags: self.mft_flags,
            mft_parent_id: self.mft_parent_id,
            mft_record_change_time: self.mft_record_change_time,
            ntfs_hard_link_count: self.ntfs_hard_link_count,
            ntfs_owner_id: self.ntfs_owner_id,
            ntfs_owner_sid: self.ntfs_owner_sid,
        }
    }
}

impl CaseObject for MftRecordFacet {
    fn class_iri() -> &'static str { MftRecordFacet::CLASS_IRI }
    fn type_name() -> &'static str { "MftRecordFacet" }
}

/// A mime part type is a grouping of characteristics unique to a component of a multi-part email body.
#[derive(Debug, Clone, Serialize)]
pub struct MimePartType {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:body")]
    pub body: Option<String>,
    #[serde(rename = "uco-observable:bodyRaw")]
    pub body_raw: Option<ObservableObject>,
    #[serde(rename = "uco-observable:contentDisposition")]
    pub content_disposition: Option<String>,
    #[serde(rename = "uco-observable:contentType")]
    pub content_type: Option<String>,
}

impl MimePartType {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/MimePartType";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MimePartTypeBuilder {
        MimePartTypeBuilder {
            body: None,
            body_raw: None,
            content_disposition: None,
            content_type: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MimePartTypeBuilder {
    body: Option<String>,
    body_raw: Option<ObservableObject>,
    content_disposition: Option<String>,
    content_type: Option<String>,
}

impl MimePartTypeBuilder {
    pub fn body(mut self, value: String) -> Self {
        self.body = Some(value);
        self
    }

    pub fn body_raw(mut self, value: ObservableObject) -> Self {
        self.body_raw = Some(value);
        self
    }

    pub fn content_disposition(mut self, value: String) -> Self {
        self.content_disposition = Some(value);
        self
    }

    pub fn content_type(mut self, value: String) -> Self {
        self.content_type = Some(value);
        self
    }

    pub fn build(self) -> MimePartType {
        MimePartType {
            class_iri: MimePartType::CLASS_IRI,
            body: self.body,
            body_raw: self.body_raw,
            content_disposition: self.content_disposition,
            content_type: self.content_type,
        }
    }
}

impl CaseObject for MimePartType {
    fn class_iri() -> &'static str { MimePartType::CLASS_IRI }
    fn type_name() -> &'static str { "MimePartType" }
}

/// A mobile account is an arrangement with an entity to enable and control the provision of some capability or service on a portable computing device. [based on https://www.lexico.com/definition/mobile_d
#[derive(Debug, Clone, Serialize)]
pub struct MobileAccount {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl MobileAccount {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/MobileAccount";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MobileAccountBuilder {
        MobileAccountBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MobileAccountBuilder {
}

impl MobileAccountBuilder {
    pub fn build(self) -> MobileAccount {
        MobileAccount {
            class_iri: MobileAccount::CLASS_IRI,
        }
    }
}

impl CaseObject for MobileAccount {
    fn class_iri() -> &'static str { MobileAccount::CLASS_IRI }
    fn type_name() -> &'static str { "MobileAccount" }
}

/// A mobile account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of some capability or service on a portable computing device. [based
#[derive(Debug, Clone, Serialize)]
pub struct MobileAccountFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:IMSI")]
    pub imsi: Option<String>,
    #[serde(rename = "uco-observable:MSISDN")]
    pub msisdn: Option<String>,
    #[serde(rename = "uco-observable:MSISDNType")]
    pub msisdn_type: Option<String>,
}

impl MobileAccountFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/MobileAccountFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MobileAccountFacetBuilder {
        MobileAccountFacetBuilder {
            imsi: None,
            msisdn: None,
            msisdn_type: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MobileAccountFacetBuilder {
    imsi: Option<String>,
    msisdn: Option<String>,
    msisdn_type: Option<String>,
}

impl MobileAccountFacetBuilder {
    pub fn imsi(mut self, value: String) -> Self {
        self.imsi = Some(value);
        self
    }

    pub fn msisdn(mut self, value: String) -> Self {
        self.msisdn = Some(value);
        self
    }

    pub fn msisdn_type(mut self, value: String) -> Self {
        self.msisdn_type = Some(value);
        self
    }

    pub fn build(self) -> MobileAccountFacet {
        MobileAccountFacet {
            class_iri: MobileAccountFacet::CLASS_IRI,
            imsi: self.imsi,
            msisdn: self.msisdn,
            msisdn_type: self.msisdn_type,
        }
    }
}

impl CaseObject for MobileAccountFacet {
    fn class_iri() -> &'static str { MobileAccountFacet::CLASS_IRI }
    fn type_name() -> &'static str { "MobileAccountFacet" }
}

/// A mobile device is a portable computing device. [based on https://www.lexico.com.definition/mobile_device]
#[derive(Debug, Clone, Serialize)]
pub struct MobileDevice {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl MobileDevice {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/MobileDevice";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MobileDeviceBuilder {
        MobileDeviceBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MobileDeviceBuilder {
}

impl MobileDeviceBuilder {
    pub fn build(self) -> MobileDevice {
        MobileDevice {
            class_iri: MobileDevice::CLASS_IRI,
        }
    }
}

impl CaseObject for MobileDevice {
    fn class_iri() -> &'static str { MobileDevice::CLASS_IRI }
    fn type_name() -> &'static str { "MobileDevice" }
}

/// A mobile device facet is a grouping of characteristics unique to a portable computing device. [based on https://www.lexico.com/definition/mobile_device]
#[derive(Debug, Clone, Serialize)]
pub struct MobileDeviceFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:ESN")]
    pub esn: Option<String>,
    #[serde(rename = "uco-observable:IMEI")]
    pub imei: Vec<String>,
    #[serde(rename = "uco-observable:bluetoothDeviceName")]
    pub bluetooth_device_name: Option<String>,
    #[serde(rename = "uco-observable:clockSetting")]
    pub clock_setting: Option<String>,
    #[serde(rename = "uco-observable:keypadUnlockCode")]
    pub keypad_unlock_code: Option<String>,
    #[serde(rename = "uco-observable:mockLocationsAllowed")]
    pub mock_locations_allowed: Option<bool>,
    #[serde(rename = "uco-observable:network")]
    pub network: Option<String>,
    #[serde(rename = "uco-observable:phoneActivationTime")]
    pub phone_activation_time: Option<String>,
    #[serde(rename = "uco-observable:storageCapacityInBytes")]
    pub storage_capacity_in_bytes: Option<i64>,
}

impl MobileDeviceFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/MobileDeviceFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MobileDeviceFacetBuilder {
        MobileDeviceFacetBuilder {
            esn: None,
            imei: Vec::new(),
            bluetooth_device_name: None,
            clock_setting: None,
            keypad_unlock_code: None,
            mock_locations_allowed: None,
            network: None,
            phone_activation_time: None,
            storage_capacity_in_bytes: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MobileDeviceFacetBuilder {
    esn: Option<String>,
    imei: Vec<String>,
    bluetooth_device_name: Option<String>,
    clock_setting: Option<String>,
    keypad_unlock_code: Option<String>,
    mock_locations_allowed: Option<bool>,
    network: Option<String>,
    phone_activation_time: Option<String>,
    storage_capacity_in_bytes: Option<i64>,
}

impl MobileDeviceFacetBuilder {
    pub fn esn(mut self, value: String) -> Self {
        self.esn = Some(value);
        self
    }

    pub fn imei(mut self, value: Vec<String>) -> Self {
        self.imei = value;
        self
    }

    pub fn bluetooth_device_name(mut self, value: String) -> Self {
        self.bluetooth_device_name = Some(value);
        self
    }

    pub fn clock_setting(mut self, value: String) -> Self {
        self.clock_setting = Some(value);
        self
    }

    pub fn keypad_unlock_code(mut self, value: String) -> Self {
        self.keypad_unlock_code = Some(value);
        self
    }

    pub fn mock_locations_allowed(mut self, value: bool) -> Self {
        self.mock_locations_allowed = Some(value);
        self
    }

    pub fn network(mut self, value: String) -> Self {
        self.network = Some(value);
        self
    }

    pub fn phone_activation_time(mut self, value: String) -> Self {
        self.phone_activation_time = Some(value);
        self
    }

    pub fn storage_capacity_in_bytes(mut self, value: i64) -> Self {
        self.storage_capacity_in_bytes = Some(value);
        self
    }

    pub fn build(self) -> MobileDeviceFacet {
        MobileDeviceFacet {
            class_iri: MobileDeviceFacet::CLASS_IRI,
            esn: self.esn,
            imei: self.imei,
            bluetooth_device_name: self.bluetooth_device_name,
            clock_setting: self.clock_setting,
            keypad_unlock_code: self.keypad_unlock_code,
            mock_locations_allowed: self.mock_locations_allowed,
            network: self.network,
            phone_activation_time: self.phone_activation_time,
            storage_capacity_in_bytes: self.storage_capacity_in_bytes,
        }
    }
}

impl CaseObject for MobileDeviceFacet {
    fn class_iri() -> &'static str { MobileDeviceFacet::CLASS_IRI }
    fn type_name() -> &'static str { "MobileDeviceFacet" }
}

/// A mobile phone is a portable telephone that at least can make and receive calls over a radio frequency link while the user is moving within a telephone service area. This category encompasses all type
#[derive(Debug, Clone, Serialize)]
pub struct MobilePhone {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl MobilePhone {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/MobilePhone";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MobilePhoneBuilder {
        MobilePhoneBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MobilePhoneBuilder {
}

impl MobilePhoneBuilder {
    pub fn build(self) -> MobilePhone {
        MobilePhone {
            class_iri: MobilePhone::CLASS_IRI,
        }
    }
}

impl CaseObject for MobilePhone {
    fn class_iri() -> &'static str { MobilePhone::CLASS_IRI }
    fn type_name() -> &'static str { "MobilePhone" }
}

/// A mutex is a mechanism that enforces limits on access to a resource when there are many threads of execution. A mutex is designed to enforce a mutual exclusion concurrency control policy, and with a v
#[derive(Debug, Clone, Serialize)]
pub struct Mutex {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Mutex {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Mutex";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MutexBuilder {
        MutexBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MutexBuilder {
}

impl MutexBuilder {
    pub fn build(self) -> Mutex {
        Mutex {
            class_iri: Mutex::CLASS_IRI,
        }
    }
}

impl CaseObject for Mutex {
    fn class_iri() -> &'static str { Mutex::CLASS_IRI }
    fn type_name() -> &'static str { "Mutex" }
}

/// A mutex facet is a grouping of characteristics unique to a mechanism that enforces limits on access to a resource when there are many threads of execution. A mutex is designed to enforce a mutual excl
#[derive(Debug, Clone, Serialize)]
pub struct MutexFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:isNamed")]
    pub is_named: Option<bool>,
    #[serde(rename = "uco-observable:mutexName")]
    pub mutex_name: Option<String>,
}

impl MutexFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/MutexFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> MutexFacetBuilder {
        MutexFacetBuilder {
            is_named: None,
            mutex_name: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct MutexFacetBuilder {
    is_named: Option<bool>,
    mutex_name: Option<String>,
}

impl MutexFacetBuilder {
    pub fn is_named(mut self, value: bool) -> Self {
        self.is_named = Some(value);
        self
    }

    pub fn mutex_name(mut self, value: String) -> Self {
        self.mutex_name = Some(value);
        self
    }

    pub fn build(self) -> MutexFacet {
        MutexFacet {
            class_iri: MutexFacet::CLASS_IRI,
            is_named: self.is_named,
            mutex_name: self.mutex_name,
        }
    }
}

impl CaseObject for MutexFacet {
    fn class_iri() -> &'static str { MutexFacet::CLASS_IRI }
    fn type_name() -> &'static str { "MutexFacet" }
}

/// An NTFS file is a New Technology File System (NTFS) file.
#[derive(Debug, Clone, Serialize)]
pub struct NTFSFile {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl NTFSFile {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NTFSFile";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> NTFSFileBuilder {
        NTFSFileBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NTFSFileBuilder {
}

impl NTFSFileBuilder {
    pub fn build(self) -> NTFSFile {
        NTFSFile {
            class_iri: NTFSFile::CLASS_IRI,
        }
    }
}

impl CaseObject for NTFSFile {
    fn class_iri() -> &'static str { NTFSFile::CLASS_IRI }
    fn type_name() -> &'static str { "NTFSFile" }
}

/// An NTFS file facet is a grouping of characteristics unique to a file on an NTFS (new technology filesystem) file system.
#[derive(Debug, Clone, Serialize)]
pub struct NTFSFileFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:alternateDataStreams")]
    pub alternate_data_streams: Vec<AlternateDataStream>,
    #[serde(rename = "uco-observable:entryID")]
    pub entry_id: Option<i64>,
    #[serde(rename = "uco-observable:sid")]
    pub sid: Option<String>,
}

impl NTFSFileFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NTFSFileFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> NTFSFileFacetBuilder {
        NTFSFileFacetBuilder {
            alternate_data_streams: Vec::new(),
            entry_id: None,
            sid: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NTFSFileFacetBuilder {
    alternate_data_streams: Vec<AlternateDataStream>,
    entry_id: Option<i64>,
    sid: Option<String>,
}

impl NTFSFileFacetBuilder {
    pub fn alternate_data_streams(mut self, value: Vec<AlternateDataStream>) -> Self {
        self.alternate_data_streams = value;
        self
    }

    pub fn entry_id(mut self, value: i64) -> Self {
        self.entry_id = Some(value);
        self
    }

    pub fn sid(mut self, value: String) -> Self {
        self.sid = Some(value);
        self
    }

    pub fn build(self) -> NTFSFileFacet {
        NTFSFileFacet {
            class_iri: NTFSFileFacet::CLASS_IRI,
            alternate_data_streams: self.alternate_data_streams,
            entry_id: self.entry_id,
            sid: self.sid,
        }
    }
}

impl CaseObject for NTFSFileFacet {
    fn class_iri() -> &'static str { NTFSFileFacet::CLASS_IRI }
    fn type_name() -> &'static str { "NTFSFileFacet" }
}

/// An NTFS file permissions facet is a grouping of characteristics unique to the access rights (e.g., view, change, navigate, execute) of a file on an NTFS (new technology filesystem) file system.
#[derive(Debug, Clone, Serialize)]
pub struct NTFSFilePermissionsFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl NTFSFilePermissionsFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NTFSFilePermissionsFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> NTFSFilePermissionsFacetBuilder {
        NTFSFilePermissionsFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NTFSFilePermissionsFacetBuilder {
}

impl NTFSFilePermissionsFacetBuilder {
    pub fn build(self) -> NTFSFilePermissionsFacet {
        NTFSFilePermissionsFacet {
            class_iri: NTFSFilePermissionsFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for NTFSFilePermissionsFacet {
    fn class_iri() -> &'static str { NTFSFilePermissionsFacet::CLASS_IRI }
    fn type_name() -> &'static str { "NTFSFilePermissionsFacet" }
}

/// A named pipe is a mechanism for FIFO (first-in-first-out) inter-process communication. It is persisted as a filesystem object (that can be deleted like any other file), can be written to or read from 
#[derive(Debug, Clone, Serialize)]
pub struct NamedPipe {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl NamedPipe {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NamedPipe";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> NamedPipeBuilder {
        NamedPipeBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NamedPipeBuilder {
}

impl NamedPipeBuilder {
    pub fn build(self) -> NamedPipe {
        NamedPipe {
            class_iri: NamedPipe::CLASS_IRI,
        }
    }
}

impl CaseObject for NamedPipe {
    fn class_iri() -> &'static str { NamedPipe::CLASS_IRI }
    fn type_name() -> &'static str { "NamedPipe" }
}

/// A network appliance is a purpose-built computer with software or firmware that is designed to provide a specific network management function.
#[derive(Debug, Clone, Serialize)]
pub struct NetworkAppliance {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl NetworkAppliance {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkAppliance";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> NetworkApplianceBuilder {
        NetworkApplianceBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NetworkApplianceBuilder {
}

impl NetworkApplianceBuilder {
    pub fn build(self) -> NetworkAppliance {
        NetworkAppliance {
            class_iri: NetworkAppliance::CLASS_IRI,
        }
    }
}

impl CaseObject for NetworkAppliance {
    fn class_iri() -> &'static str { NetworkAppliance::CLASS_IRI }
    fn type_name() -> &'static str { "NetworkAppliance" }
}

/// A network connection is a connection (completed or attempted) across a digital network (a group of two or more computer systems linked together). [based on https://www.webopedia.com/TERM/N/network.htm
#[derive(Debug, Clone, Serialize)]
pub struct NetworkConnection {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl NetworkConnection {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkConnection";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> NetworkConnectionBuilder {
        NetworkConnectionBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NetworkConnectionBuilder {
}

impl NetworkConnectionBuilder {
    pub fn build(self) -> NetworkConnection {
        NetworkConnection {
            class_iri: NetworkConnection::CLASS_IRI,
        }
    }
}

impl CaseObject for NetworkConnection {
    fn class_iri() -> &'static str { NetworkConnection::CLASS_IRI }
    fn type_name() -> &'static str { "NetworkConnection" }
}

/// A network connection facet is a grouping of characteristics unique to a connection (complete or attempted) accross a digital network (a group of two or more computer systems linked together). [based o
#[derive(Debug, Clone, Serialize)]
pub struct NetworkConnectionFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:destinationPort")]
    pub destination_port: Option<i64>,
    #[serde(rename = "uco-observable:dst")]
    pub dst: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:endTime")]
    pub end_time: Option<String>,
    #[serde(rename = "uco-observable:isActive")]
    pub is_active: Option<bool>,
    #[serde(rename = "uco-observable:protocols")]
    pub protocols: Option<ControlledDictionary>,
    #[serde(rename = "uco-observable:sourcePort")]
    pub source_port: Option<i64>,
    #[serde(rename = "uco-observable:src")]
    pub src: Vec<UcoObject>,
    #[serde(rename = "uco-observable:startTime")]
    pub start_time: Option<String>,
}

impl NetworkConnectionFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkConnectionFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> NetworkConnectionFacetBuilder {
        NetworkConnectionFacetBuilder {
            destination_port: None,
            dst: Vec::new(),
            end_time: None,
            is_active: None,
            protocols: None,
            source_port: None,
            src: Vec::new(),
            start_time: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NetworkConnectionFacetBuilder {
    destination_port: Option<i64>,
    dst: Vec<ObservableObject>,
    end_time: Option<String>,
    is_active: Option<bool>,
    protocols: Option<ControlledDictionary>,
    source_port: Option<i64>,
    src: Vec<UcoObject>,
    start_time: Option<String>,
}

impl NetworkConnectionFacetBuilder {
    pub fn destination_port(mut self, value: i64) -> Self {
        self.destination_port = Some(value);
        self
    }

    pub fn dst(mut self, value: Vec<ObservableObject>) -> Self {
        self.dst = value;
        self
    }

    pub fn end_time(mut self, value: String) -> Self {
        self.end_time = Some(value);
        self
    }

    pub fn is_active(mut self, value: bool) -> Self {
        self.is_active = Some(value);
        self
    }

    pub fn protocols(mut self, value: ControlledDictionary) -> Self {
        self.protocols = Some(value);
        self
    }

    pub fn source_port(mut self, value: i64) -> Self {
        self.source_port = Some(value);
        self
    }

    pub fn src(mut self, value: Vec<UcoObject>) -> Self {
        self.src = value;
        self
    }

    pub fn start_time(mut self, value: String) -> Self {
        self.start_time = Some(value);
        self
    }

    pub fn build(self) -> NetworkConnectionFacet {
        NetworkConnectionFacet {
            class_iri: NetworkConnectionFacet::CLASS_IRI,
            destination_port: self.destination_port,
            dst: self.dst,
            end_time: self.end_time,
            is_active: self.is_active,
            protocols: self.protocols,
            source_port: self.source_port,
            src: self.src,
            start_time: self.start_time,
        }
    }
}

impl CaseObject for NetworkConnectionFacet {
    fn class_iri() -> &'static str { NetworkConnectionFacet::CLASS_IRI }
    fn type_name() -> &'static str { "NetworkConnectionFacet" }
}

/// A network flow is a sequence of data transiting one or more digital network (a group or two or more computer systems linked together) connections. [based on https://www.webopedia.com/TERM/N/network.ht
#[derive(Debug, Clone, Serialize)]
pub struct NetworkFlow {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl NetworkFlow {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkFlow";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> NetworkFlowBuilder {
        NetworkFlowBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NetworkFlowBuilder {
}

impl NetworkFlowBuilder {
    pub fn build(self) -> NetworkFlow {
        NetworkFlow {
            class_iri: NetworkFlow::CLASS_IRI,
        }
    }
}

impl CaseObject for NetworkFlow {
    fn class_iri() -> &'static str { NetworkFlow::CLASS_IRI }
    fn type_name() -> &'static str { "NetworkFlow" }
}

/// A network flow facet is a grouping of characteristics unique to a sequence of data transiting one or more digital network (a group of two or more computer systems linked together) connections. [based 
#[derive(Debug, Clone, Serialize)]
pub struct NetworkFlowFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:dstBytes")]
    pub dst_bytes: Option<i64>,
    #[serde(rename = "uco-observable:dstPackets")]
    pub dst_packets: Option<i64>,
    #[serde(rename = "uco-observable:dstPayload")]
    pub dst_payload: Option<ObservableObject>,
    #[serde(rename = "uco-observable:ipfix")]
    pub ipfix: Option<Dictionary>,
    #[serde(rename = "uco-observable:srcBytes")]
    pub src_bytes: Option<i64>,
    #[serde(rename = "uco-observable:srcPackets")]
    pub src_packets: Option<i64>,
    #[serde(rename = "uco-observable:srcPayload")]
    pub src_payload: Option<ObservableObject>,
}

impl NetworkFlowFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkFlowFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> NetworkFlowFacetBuilder {
        NetworkFlowFacetBuilder {
            dst_bytes: None,
            dst_packets: None,
            dst_payload: None,
            ipfix: None,
            src_bytes: None,
            src_packets: None,
            src_payload: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NetworkFlowFacetBuilder {
    dst_bytes: Option<i64>,
    dst_packets: Option<i64>,
    dst_payload: Option<ObservableObject>,
    ipfix: Option<Dictionary>,
    src_bytes: Option<i64>,
    src_packets: Option<i64>,
    src_payload: Option<ObservableObject>,
}

impl NetworkFlowFacetBuilder {
    pub fn dst_bytes(mut self, value: i64) -> Self {
        self.dst_bytes = Some(value);
        self
    }

    pub fn dst_packets(mut self, value: i64) -> Self {
        self.dst_packets = Some(value);
        self
    }

    pub fn dst_payload(mut self, value: ObservableObject) -> Self {
        self.dst_payload = Some(value);
        self
    }

    pub fn ipfix(mut self, value: Dictionary) -> Self {
        self.ipfix = Some(value);
        self
    }

    pub fn src_bytes(mut self, value: i64) -> Self {
        self.src_bytes = Some(value);
        self
    }

    pub fn src_packets(mut self, value: i64) -> Self {
        self.src_packets = Some(value);
        self
    }

    pub fn src_payload(mut self, value: ObservableObject) -> Self {
        self.src_payload = Some(value);
        self
    }

    pub fn build(self) -> NetworkFlowFacet {
        NetworkFlowFacet {
            class_iri: NetworkFlowFacet::CLASS_IRI,
            dst_bytes: self.dst_bytes,
            dst_packets: self.dst_packets,
            dst_payload: self.dst_payload,
            ipfix: self.ipfix,
            src_bytes: self.src_bytes,
            src_packets: self.src_packets,
            src_payload: self.src_payload,
        }
    }
}

impl CaseObject for NetworkFlowFacet {
    fn class_iri() -> &'static str { NetworkFlowFacet::CLASS_IRI }
    fn type_name() -> &'static str { "NetworkFlowFacet" }
}

/// A network interface is a software or hardware interface between two pieces of equipment or protocol layers in a computer network.
#[derive(Debug, Clone, Serialize)]
pub struct NetworkInterface {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl NetworkInterface {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkInterface";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> NetworkInterfaceBuilder {
        NetworkInterfaceBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NetworkInterfaceBuilder {
}

impl NetworkInterfaceBuilder {
    pub fn build(self) -> NetworkInterface {
        NetworkInterface {
            class_iri: NetworkInterface::CLASS_IRI,
        }
    }
}

impl CaseObject for NetworkInterface {
    fn class_iri() -> &'static str { NetworkInterface::CLASS_IRI }
    fn type_name() -> &'static str { "NetworkInterface" }
}

/// A network interface facet is a grouping of characteristics unique to a software or hardware interface between two pieces of equipment or protocol layers in a computer network.
#[derive(Debug, Clone, Serialize)]
pub struct NetworkInterfaceFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:adapterName")]
    pub adapter_name: Option<String>,
    #[serde(rename = "uco-observable:dhcpLeaseExpires")]
    pub dhcp_lease_expires: Option<String>,
    #[serde(rename = "uco-observable:dhcpLeaseObtained")]
    pub dhcp_lease_obtained: Option<String>,
    #[serde(rename = "uco-observable:dhcpServer")]
    pub dhcp_server: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:ip")]
    pub ip: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:ipGateway")]
    pub ip_gateway: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:macAddress")]
    pub mac_address: Option<ObservableObject>,
}

impl NetworkInterfaceFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkInterfaceFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> NetworkInterfaceFacetBuilder {
        NetworkInterfaceFacetBuilder {
            adapter_name: None,
            dhcp_lease_expires: None,
            dhcp_lease_obtained: None,
            dhcp_server: Vec::new(),
            ip: Vec::new(),
            ip_gateway: Vec::new(),
            mac_address: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NetworkInterfaceFacetBuilder {
    adapter_name: Option<String>,
    dhcp_lease_expires: Option<String>,
    dhcp_lease_obtained: Option<String>,
    dhcp_server: Vec<ObservableObject>,
    ip: Vec<ObservableObject>,
    ip_gateway: Vec<ObservableObject>,
    mac_address: Option<ObservableObject>,
}

impl NetworkInterfaceFacetBuilder {
    pub fn adapter_name(mut self, value: String) -> Self {
        self.adapter_name = Some(value);
        self
    }

    pub fn dhcp_lease_expires(mut self, value: String) -> Self {
        self.dhcp_lease_expires = Some(value);
        self
    }

    pub fn dhcp_lease_obtained(mut self, value: String) -> Self {
        self.dhcp_lease_obtained = Some(value);
        self
    }

    pub fn dhcp_server(mut self, value: Vec<ObservableObject>) -> Self {
        self.dhcp_server = value;
        self
    }

    pub fn ip(mut self, value: Vec<ObservableObject>) -> Self {
        self.ip = value;
        self
    }

    pub fn ip_gateway(mut self, value: Vec<ObservableObject>) -> Self {
        self.ip_gateway = value;
        self
    }

    pub fn mac_address(mut self, value: ObservableObject) -> Self {
        self.mac_address = Some(value);
        self
    }

    pub fn build(self) -> NetworkInterfaceFacet {
        NetworkInterfaceFacet {
            class_iri: NetworkInterfaceFacet::CLASS_IRI,
            adapter_name: self.adapter_name,
            dhcp_lease_expires: self.dhcp_lease_expires,
            dhcp_lease_obtained: self.dhcp_lease_obtained,
            dhcp_server: self.dhcp_server,
            ip: self.ip,
            ip_gateway: self.ip_gateway,
            mac_address: self.mac_address,
        }
    }
}

impl CaseObject for NetworkInterfaceFacet {
    fn class_iri() -> &'static str { NetworkInterfaceFacet::CLASS_IRI }
    fn type_name() -> &'static str { "NetworkInterfaceFacet" }
}

/// A network protocol is an established set of structured rules that determine how data is transmitted between different devices in the same network. Essentially, it allows connected devices to communica
#[derive(Debug, Clone, Serialize)]
pub struct NetworkProtocol {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl NetworkProtocol {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkProtocol";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> NetworkProtocolBuilder {
        NetworkProtocolBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NetworkProtocolBuilder {
}

impl NetworkProtocolBuilder {
    pub fn build(self) -> NetworkProtocol {
        NetworkProtocol {
            class_iri: NetworkProtocol::CLASS_IRI,
        }
    }
}

impl CaseObject for NetworkProtocol {
    fn class_iri() -> &'static str { NetworkProtocol::CLASS_IRI }
    fn type_name() -> &'static str { "NetworkProtocol" }
}

/// A network route is a specific path (of specific network nodes, connections and protocols) for traffic in a network or between or across multiple networks.
#[derive(Debug, Clone, Serialize)]
pub struct NetworkRoute {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl NetworkRoute {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkRoute";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> NetworkRouteBuilder {
        NetworkRouteBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NetworkRouteBuilder {
}

impl NetworkRouteBuilder {
    pub fn build(self) -> NetworkRoute {
        NetworkRoute {
            class_iri: NetworkRoute::CLASS_IRI,
        }
    }
}

impl CaseObject for NetworkRoute {
    fn class_iri() -> &'static str { NetworkRoute::CLASS_IRI }
    fn type_name() -> &'static str { "NetworkRoute" }
}

/// A network subnet is a logical subdivision of an IP network. [based on https://en.wikipedia.org/wiki/Subnetwork]
#[derive(Debug, Clone, Serialize)]
pub struct NetworkSubnet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl NetworkSubnet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NetworkSubnet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> NetworkSubnetBuilder {
        NetworkSubnetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NetworkSubnetBuilder {
}

impl NetworkSubnetBuilder {
    pub fn build(self) -> NetworkSubnet {
        NetworkSubnet {
            class_iri: NetworkSubnet::CLASS_IRI,
        }
    }
}

impl CaseObject for NetworkSubnet {
    fn class_iri() -> &'static str { NetworkSubnet::CLASS_IRI }
    fn type_name() -> &'static str { "NetworkSubnet" }
}

/// A note is a brief textual record.
#[derive(Debug, Clone, Serialize)]
pub struct Note {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Note {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Note";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> NoteBuilder {
        NoteBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NoteBuilder {
}

impl NoteBuilder {
    pub fn build(self) -> Note {
        Note {
            class_iri: Note::CLASS_IRI,
        }
    }
}

impl CaseObject for Note {
    fn class_iri() -> &'static str { Note::CLASS_IRI }
    fn type_name() -> &'static str { "Note" }
}

/// A note facet is a grouping of characteristics unique to a brief textual record.
#[derive(Debug, Clone, Serialize)]
pub struct NoteFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:application")]
    pub application: Option<ObservableObject>,
    #[serde(rename = "uco-observable:modifiedTime")]
    pub modified_time: Option<String>,
    #[serde(rename = "uco-observable:observableCreatedTime")]
    pub observable_created_time: Option<String>,
    #[serde(rename = "uco-observable:text")]
    pub text: Option<String>,
}

impl NoteFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/NoteFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> NoteFacetBuilder {
        NoteFacetBuilder {
            application: None,
            modified_time: None,
            observable_created_time: None,
            text: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct NoteFacetBuilder {
    application: Option<ObservableObject>,
    modified_time: Option<String>,
    observable_created_time: Option<String>,
    text: Option<String>,
}

impl NoteFacetBuilder {
    pub fn application(mut self, value: ObservableObject) -> Self {
        self.application = Some(value);
        self
    }

    pub fn modified_time(mut self, value: String) -> Self {
        self.modified_time = Some(value);
        self
    }

    pub fn observable_created_time(mut self, value: String) -> Self {
        self.observable_created_time = Some(value);
        self
    }

    pub fn text(mut self, value: String) -> Self {
        self.text = Some(value);
        self
    }

    pub fn build(self) -> NoteFacet {
        NoteFacet {
            class_iri: NoteFacet::CLASS_IRI,
            application: self.application,
            modified_time: self.modified_time,
            observable_created_time: self.observable_created_time,
            text: self.text,
        }
    }
}

impl CaseObject for NoteFacet {
    fn class_iri() -> &'static str { NoteFacet::CLASS_IRI }
    fn type_name() -> &'static str { "NoteFacet" }
}

/// An observable is a characterizable item or action within the digital domain.
#[derive(Debug, Clone, Serialize)]
pub struct Observable {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Observable {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Observable";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ObservableBuilder {
        ObservableBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ObservableBuilder {
}

impl ObservableBuilder {
    pub fn build(self) -> Observable {
        Observable {
            class_iri: Observable::CLASS_IRI,
        }
    }
}

impl CaseObject for Observable {
    fn class_iri() -> &'static str { Observable::CLASS_IRI }
    fn type_name() -> &'static str { "Observable" }
}

/// An observable action is a grouping of characteristics unique to something that may be done or performed within the digital domain.
#[derive(Debug, Clone, Serialize)]
pub struct ObservableAction {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ObservableAction {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ObservableAction";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ObservableActionBuilder {
        ObservableActionBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ObservableActionBuilder {
}

impl ObservableActionBuilder {
    pub fn build(self) -> ObservableAction {
        ObservableAction {
            class_iri: ObservableAction::CLASS_IRI,
        }
    }
}

impl CaseObject for ObservableAction {
    fn class_iri() -> &'static str { ObservableAction::CLASS_IRI }
    fn type_name() -> &'static str { "ObservableAction" }
}

/// An observable object is a grouping of characteristics unique to a distinct article or unit within the digital domain.
#[derive(Debug, Clone, Serialize)]
pub struct ObservableObject {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:hasChanged")]
    pub has_changed: Option<bool>,
    #[serde(rename = "uco-observable:state")]
    pub state: Option<String>,
}

impl ObservableObject {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ObservableObject";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ObservableObjectBuilder {
        ObservableObjectBuilder {
            has_changed: None,
            state: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ObservableObjectBuilder {
    has_changed: Option<bool>,
    state: Option<String>,
}

impl ObservableObjectBuilder {
    pub fn has_changed(mut self, value: bool) -> Self {
        self.has_changed = Some(value);
        self
    }

    pub fn state(mut self, value: String) -> Self {
        self.state = Some(value);
        self
    }

    pub fn build(self) -> ObservableObject {
        ObservableObject {
            class_iri: ObservableObject::CLASS_IRI,
            has_changed: self.has_changed,
            state: self.state,
        }
    }
}

impl CaseObject for ObservableObject {
    fn class_iri() -> &'static str { ObservableObject::CLASS_IRI }
    fn type_name() -> &'static str { "ObservableObject" }
}

/// An observable pattern is a grouping of characteristics unique to a logical pattern composed of observable object and observable action properties.
#[derive(Debug, Clone, Serialize)]
pub struct ObservablePattern {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ObservablePattern {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ObservablePattern";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ObservablePatternBuilder {
        ObservablePatternBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ObservablePatternBuilder {
}

impl ObservablePatternBuilder {
    pub fn build(self) -> ObservablePattern {
        ObservablePattern {
            class_iri: ObservablePattern::CLASS_IRI,
        }
    }
}

impl CaseObject for ObservablePattern {
    fn class_iri() -> &'static str { ObservablePattern::CLASS_IRI }
    fn type_name() -> &'static str { "ObservablePattern" }
}

/// An observable relationship is a grouping of characteristics unique to an assertion of an association between two observable objects.
#[derive(Debug, Clone, Serialize)]
pub struct ObservableRelationship {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:source")]
    pub source: Vec<Observable>,
    #[serde(rename = "uco-core:target")]
    pub target: Vec<Observable>,
}

impl ObservableRelationship {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ObservableRelationship";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ObservableRelationshipBuilder {
        ObservableRelationshipBuilder {
            source: Vec::new(),
            target: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ObservableRelationshipBuilder {
    source: Vec<Observable>,
    target: Vec<Observable>,
}

impl ObservableRelationshipBuilder {
    pub fn source(mut self, value: Vec<Observable>) -> Self {
        self.source = value;
        self
    }

    pub fn target(mut self, value: Vec<Observable>) -> Self {
        self.target = value;
        self
    }

    pub fn build(self) -> ObservableRelationship {
        ObservableRelationship {
            class_iri: ObservableRelationship::CLASS_IRI,
            source: self.source,
            target: self.target,
        }
    }
}

impl CaseObject for ObservableRelationship {
    fn class_iri() -> &'static str { ObservableRelationship::CLASS_IRI }
    fn type_name() -> &'static str { "ObservableRelationship" }
}

/// An observation is a temporal perception of an observable.
#[derive(Debug, Clone, Serialize)]
pub struct Observation {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:name")]
    pub name: String,
}

impl Observation {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Observation";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ObservationBuilder {
        ObservationBuilder {
            name: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ObservationBuilder {
    name: Option<String>,
}

impl ObservationBuilder {
    pub fn name(mut self, value: String) -> Self {
        self.name = Some(value);
        self
    }

    pub fn build(self) -> Observation {
        Observation {
            class_iri: Observation::CLASS_IRI,
            name: self.name.expect("missing required field: name"),
        }
    }
}

impl CaseObject for Observation {
    fn class_iri() -> &'static str { Observation::CLASS_IRI }
    fn type_name() -> &'static str { "Observation" }
}

/// An online service is a particular provision mechanism of information access, distribution or manipulation over the Internet.
#[derive(Debug, Clone, Serialize)]
pub struct OnlineService {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl OnlineService {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/OnlineService";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> OnlineServiceBuilder {
        OnlineServiceBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct OnlineServiceBuilder {
}

impl OnlineServiceBuilder {
    pub fn build(self) -> OnlineService {
        OnlineService {
            class_iri: OnlineService::CLASS_IRI,
        }
    }
}

impl CaseObject for OnlineService {
    fn class_iri() -> &'static str { OnlineService::CLASS_IRI }
    fn type_name() -> &'static str { "OnlineService" }
}

/// An online service facet is a grouping of characteristics unique to a particular provision mechanism of information access, distribution or manipulation over the Internet.
#[derive(Debug, Clone, Serialize)]
pub struct OnlineServiceFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:name")]
    pub name: Option<String>,
    #[serde(rename = "uco-observable:inetLocation")]
    pub inet_location: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:location")]
    pub location: Vec<Location>,
}

impl OnlineServiceFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/OnlineServiceFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> OnlineServiceFacetBuilder {
        OnlineServiceFacetBuilder {
            name: None,
            inet_location: Vec::new(),
            location: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct OnlineServiceFacetBuilder {
    name: Option<String>,
    inet_location: Vec<ObservableObject>,
    location: Vec<Location>,
}

impl OnlineServiceFacetBuilder {
    pub fn name(mut self, value: String) -> Self {
        self.name = Some(value);
        self
    }

    pub fn inet_location(mut self, value: Vec<ObservableObject>) -> Self {
        self.inet_location = value;
        self
    }

    pub fn location(mut self, value: Vec<Location>) -> Self {
        self.location = value;
        self
    }

    pub fn build(self) -> OnlineServiceFacet {
        OnlineServiceFacet {
            class_iri: OnlineServiceFacet::CLASS_IRI,
            name: self.name,
            inet_location: self.inet_location,
            location: self.location,
        }
    }
}

impl CaseObject for OnlineServiceFacet {
    fn class_iri() -> &'static str { OnlineServiceFacet::CLASS_IRI }
    fn type_name() -> &'static str { "OnlineServiceFacet" }
}

/// An operating system is the software that manages computer hardware, software resources, and provides common services for computer programs. [based on https://en.wikipedia.org/wiki/Operating_system]
#[derive(Debug, Clone, Serialize)]
pub struct OperatingSystem {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl OperatingSystem {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/OperatingSystem";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> OperatingSystemBuilder {
        OperatingSystemBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct OperatingSystemBuilder {
}

impl OperatingSystemBuilder {
    pub fn build(self) -> OperatingSystem {
        OperatingSystem {
            class_iri: OperatingSystem::CLASS_IRI,
        }
    }
}

impl CaseObject for OperatingSystem {
    fn class_iri() -> &'static str { OperatingSystem::CLASS_IRI }
    fn type_name() -> &'static str { "OperatingSystem" }
}

/// An operating system facet is a grouping of characteristics unique to the software that manages computer hardware, software resources, and provides common services for computer programs. [based on http
#[derive(Debug, Clone, Serialize)]
pub struct OperatingSystemFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:advertisingID")]
    pub advertising_id: Vec<String>,
    #[serde(rename = "uco-observable:bitness")]
    pub bitness: Option<String>,
    #[serde(rename = "uco-observable:environmentVariables")]
    pub environment_variables: Option<Dictionary>,
    #[serde(rename = "uco-observable:installDate")]
    pub install_date: Option<String>,
    #[serde(rename = "uco-observable:isLimitAdTrackingEnabled")]
    pub is_limit_ad_tracking_enabled: Option<bool>,
    #[serde(rename = "uco-observable:manufacturer")]
    pub manufacturer: Option<Identity>,
    #[serde(rename = "uco-observable:version")]
    pub version: Option<String>,
}

impl OperatingSystemFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/OperatingSystemFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> OperatingSystemFacetBuilder {
        OperatingSystemFacetBuilder {
            advertising_id: Vec::new(),
            bitness: None,
            environment_variables: None,
            install_date: None,
            is_limit_ad_tracking_enabled: None,
            manufacturer: None,
            version: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct OperatingSystemFacetBuilder {
    advertising_id: Vec<String>,
    bitness: Option<String>,
    environment_variables: Option<Dictionary>,
    install_date: Option<String>,
    is_limit_ad_tracking_enabled: Option<bool>,
    manufacturer: Option<Identity>,
    version: Option<String>,
}

impl OperatingSystemFacetBuilder {
    pub fn advertising_id(mut self, value: Vec<String>) -> Self {
        self.advertising_id = value;
        self
    }

    pub fn bitness(mut self, value: String) -> Self {
        self.bitness = Some(value);
        self
    }

    pub fn environment_variables(mut self, value: Dictionary) -> Self {
        self.environment_variables = Some(value);
        self
    }

    pub fn install_date(mut self, value: String) -> Self {
        self.install_date = Some(value);
        self
    }

    pub fn is_limit_ad_tracking_enabled(mut self, value: bool) -> Self {
        self.is_limit_ad_tracking_enabled = Some(value);
        self
    }

    pub fn manufacturer(mut self, value: Identity) -> Self {
        self.manufacturer = Some(value);
        self
    }

    pub fn version(mut self, value: String) -> Self {
        self.version = Some(value);
        self
    }

    pub fn build(self) -> OperatingSystemFacet {
        OperatingSystemFacet {
            class_iri: OperatingSystemFacet::CLASS_IRI,
            advertising_id: self.advertising_id,
            bitness: self.bitness,
            environment_variables: self.environment_variables,
            install_date: self.install_date,
            is_limit_ad_tracking_enabled: self.is_limit_ad_tracking_enabled,
            manufacturer: self.manufacturer,
            version: self.version,
        }
    }
}

impl CaseObject for OperatingSystemFacet {
    fn class_iri() -> &'static str { OperatingSystemFacet::CLASS_IRI }
    fn type_name() -> &'static str { "OperatingSystemFacet" }
}

/// A PDF file is a Portable Document Format (PDF) file.
#[derive(Debug, Clone, Serialize)]
pub struct PDFFile {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl PDFFile {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/PDFFile";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> PDFFileBuilder {
        PDFFileBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct PDFFileBuilder {
}

impl PDFFileBuilder {
    pub fn build(self) -> PDFFile {
        PDFFile {
            class_iri: PDFFile::CLASS_IRI,
        }
    }
}

impl CaseObject for PDFFile {
    fn class_iri() -> &'static str { PDFFile::CLASS_IRI }
    fn type_name() -> &'static str { "PDFFile" }
}

/// A PDF file facet is a grouping of characteristics unique to a PDF (Portable Document Format) file.
#[derive(Debug, Clone, Serialize)]
pub struct PDFFileFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:documentInformationDictionary")]
    pub document_information_dictionary: Option<ControlledDictionary>,
    #[serde(rename = "uco-observable:isOptimized")]
    pub is_optimized: Option<bool>,
    #[serde(rename = "uco-observable:pdfCreationDate")]
    pub pdf_creation_date: Option<String>,
    #[serde(rename = "uco-observable:pdfId0")]
    pub pdf_id0: Vec<String>,
    #[serde(rename = "uco-observable:pdfId1")]
    pub pdf_id1: Option<String>,
    #[serde(rename = "uco-observable:pdfModDate")]
    pub pdf_mod_date: Option<String>,
    #[serde(rename = "uco-observable:version")]
    pub version: Option<String>,
}

impl PDFFileFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/PDFFileFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> PDFFileFacetBuilder {
        PDFFileFacetBuilder {
            document_information_dictionary: None,
            is_optimized: None,
            pdf_creation_date: None,
            pdf_id0: Vec::new(),
            pdf_id1: None,
            pdf_mod_date: None,
            version: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct PDFFileFacetBuilder {
    document_information_dictionary: Option<ControlledDictionary>,
    is_optimized: Option<bool>,
    pdf_creation_date: Option<String>,
    pdf_id0: Vec<String>,
    pdf_id1: Option<String>,
    pdf_mod_date: Option<String>,
    version: Option<String>,
}

impl PDFFileFacetBuilder {
    pub fn document_information_dictionary(mut self, value: ControlledDictionary) -> Self {
        self.document_information_dictionary = Some(value);
        self
    }

    pub fn is_optimized(mut self, value: bool) -> Self {
        self.is_optimized = Some(value);
        self
    }

    pub fn pdf_creation_date(mut self, value: String) -> Self {
        self.pdf_creation_date = Some(value);
        self
    }

    pub fn pdf_id0(mut self, value: Vec<String>) -> Self {
        self.pdf_id0 = value;
        self
    }

    pub fn pdf_id1(mut self, value: String) -> Self {
        self.pdf_id1 = Some(value);
        self
    }

    pub fn pdf_mod_date(mut self, value: String) -> Self {
        self.pdf_mod_date = Some(value);
        self
    }

    pub fn version(mut self, value: String) -> Self {
        self.version = Some(value);
        self
    }

    pub fn build(self) -> PDFFileFacet {
        PDFFileFacet {
            class_iri: PDFFileFacet::CLASS_IRI,
            document_information_dictionary: self.document_information_dictionary,
            is_optimized: self.is_optimized,
            pdf_creation_date: self.pdf_creation_date,
            pdf_id0: self.pdf_id0,
            pdf_id1: self.pdf_id1,
            pdf_mod_date: self.pdf_mod_date,
            version: self.version,
        }
    }
}

impl CaseObject for PDFFileFacet {
    fn class_iri() -> &'static str { PDFFileFacet::CLASS_IRI }
    fn type_name() -> &'static str { "PDFFileFacet" }
}

/// A path relation facet is a grouping of characteristics unique to the location of one object within another containing object.
#[derive(Debug, Clone, Serialize)]
pub struct PathRelationFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:path")]
    pub path: Vec<String>,
}

impl PathRelationFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/PathRelationFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> PathRelationFacetBuilder {
        PathRelationFacetBuilder {
            path: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct PathRelationFacetBuilder {
    path: Vec<String>,
}

impl PathRelationFacetBuilder {
    pub fn path(mut self, value: Vec<String>) -> Self {
        self.path = value;
        self
    }

    pub fn build(self) -> PathRelationFacet {
        PathRelationFacet {
            class_iri: PathRelationFacet::CLASS_IRI,
            path: self.path,
        }
    }
}

impl CaseObject for PathRelationFacet {
    fn class_iri() -> &'static str { PathRelationFacet::CLASS_IRI }
    fn type_name() -> &'static str { "PathRelationFacet" }
}

/// A payment card is a physical token that is part of a payment system issued by financial institutions, such as a bank, to a customer that enables its owner (the cardholder) to access the funds in the c
#[derive(Debug, Clone, Serialize)]
pub struct PaymentCard {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl PaymentCard {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/PaymentCard";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> PaymentCardBuilder {
        PaymentCardBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct PaymentCardBuilder {
}

impl PaymentCardBuilder {
    pub fn build(self) -> PaymentCard {
        PaymentCard {
            class_iri: PaymentCard::CLASS_IRI,
        }
    }
}

impl CaseObject for PaymentCard {
    fn class_iri() -> &'static str { PaymentCard::CLASS_IRI }
    fn type_name() -> &'static str { "PaymentCard" }
}

/// A phone account is an arrangement with an entity to enable and control the provision of a telephony capability or service.
#[derive(Debug, Clone, Serialize)]
pub struct PhoneAccount {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl PhoneAccount {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/PhoneAccount";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> PhoneAccountBuilder {
        PhoneAccountBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct PhoneAccountBuilder {
}

impl PhoneAccountBuilder {
    pub fn build(self) -> PhoneAccount {
        PhoneAccount {
            class_iri: PhoneAccount::CLASS_IRI,
        }
    }
}

impl CaseObject for PhoneAccount {
    fn class_iri() -> &'static str { PhoneAccount::CLASS_IRI }
    fn type_name() -> &'static str { "PhoneAccount" }
}

/// A phone account facet is a grouping of characteristics unique to an arrangement with an entity to enable and control the provision of a telephony capability or service.
#[derive(Debug, Clone, Serialize)]
pub struct PhoneAccountFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:phoneNumber")]
    pub phone_number: Option<String>,
}

impl PhoneAccountFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/PhoneAccountFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> PhoneAccountFacetBuilder {
        PhoneAccountFacetBuilder {
            phone_number: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct PhoneAccountFacetBuilder {
    phone_number: Option<String>,
}

impl PhoneAccountFacetBuilder {
    pub fn phone_number(mut self, value: String) -> Self {
        self.phone_number = Some(value);
        self
    }

    pub fn build(self) -> PhoneAccountFacet {
        PhoneAccountFacet {
            class_iri: PhoneAccountFacet::CLASS_IRI,
            phone_number: self.phone_number,
        }
    }
}

impl CaseObject for PhoneAccountFacet {
    fn class_iri() -> &'static str { PhoneAccountFacet::CLASS_IRI }
    fn type_name() -> &'static str { "PhoneAccountFacet" }
}

/// A pipe is a mechanism for one-way inter-process communication using message passing where data written by one process is buffered by the operating system until it is read by the next process, and this
#[derive(Debug, Clone, Serialize)]
pub struct Pipe {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Pipe {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Pipe";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> PipeBuilder {
        PipeBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct PipeBuilder {
}

impl PipeBuilder {
    pub fn build(self) -> Pipe {
        Pipe {
            class_iri: Pipe::CLASS_IRI,
        }
    }
}

impl CaseObject for Pipe {
    fn class_iri() -> &'static str { Pipe::CLASS_IRI }
    fn type_name() -> &'static str { "Pipe" }
}

/// A post is message submitted to an online discussion/publishing site (forum, blog, etc.).
#[derive(Debug, Clone, Serialize)]
pub struct Post {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Post {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Post";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> PostBuilder {
        PostBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct PostBuilder {
}

impl PostBuilder {
    pub fn build(self) -> Post {
        Post {
            class_iri: Post::CLASS_IRI,
        }
    }
}

impl CaseObject for Post {
    fn class_iri() -> &'static str { Post::CLASS_IRI }
    fn type_name() -> &'static str { "Post" }
}

/// A process is an instance of a computer program executed on an operating system.
#[derive(Debug, Clone, Serialize)]
pub struct Process {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Process {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Process";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ProcessBuilder {
        ProcessBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ProcessBuilder {
}

impl ProcessBuilder {
    pub fn build(self) -> Process {
        Process {
            class_iri: Process::CLASS_IRI,
        }
    }
}

impl CaseObject for Process {
    fn class_iri() -> &'static str { Process::CLASS_IRI }
    fn type_name() -> &'static str { "Process" }
}

/// A process facet is a grouping of characteristics unique to an instance of a computer program executed on an operating system.
#[derive(Debug, Clone, Serialize)]
pub struct ProcessFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:arguments")]
    pub arguments: Vec<String>,
    #[serde(rename = "uco-observable:binary")]
    pub binary: Option<ObservableObject>,
    #[serde(rename = "uco-observable:creatorUser")]
    pub creator_user: Option<ObservableObject>,
    #[serde(rename = "uco-observable:currentWorkingDirectory")]
    pub current_working_directory: Option<String>,
    #[serde(rename = "uco-observable:environmentVariables")]
    pub environment_variables: Option<Dictionary>,
    #[serde(rename = "uco-observable:exitStatus")]
    pub exit_status: Option<i64>,
    #[serde(rename = "uco-observable:exitTime")]
    pub exit_time: Option<String>,
    #[serde(rename = "uco-observable:isHidden")]
    pub is_hidden: Option<bool>,
    #[serde(rename = "uco-observable:observableCreatedTime")]
    pub observable_created_time: Option<String>,
    #[serde(rename = "uco-observable:parent")]
    pub parent: Option<ObservableObject>,
    #[serde(rename = "uco-observable:pid")]
    pub pid: Option<i64>,
    #[serde(rename = "uco-observable:status")]
    pub status: Option<String>,
}

impl ProcessFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ProcessFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ProcessFacetBuilder {
        ProcessFacetBuilder {
            arguments: Vec::new(),
            binary: None,
            creator_user: None,
            current_working_directory: None,
            environment_variables: None,
            exit_status: None,
            exit_time: None,
            is_hidden: None,
            observable_created_time: None,
            parent: None,
            pid: None,
            status: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ProcessFacetBuilder {
    arguments: Vec<String>,
    binary: Option<ObservableObject>,
    creator_user: Option<ObservableObject>,
    current_working_directory: Option<String>,
    environment_variables: Option<Dictionary>,
    exit_status: Option<i64>,
    exit_time: Option<String>,
    is_hidden: Option<bool>,
    observable_created_time: Option<String>,
    parent: Option<ObservableObject>,
    pid: Option<i64>,
    status: Option<String>,
}

impl ProcessFacetBuilder {
    pub fn arguments(mut self, value: Vec<String>) -> Self {
        self.arguments = value;
        self
    }

    pub fn binary(mut self, value: ObservableObject) -> Self {
        self.binary = Some(value);
        self
    }

    pub fn creator_user(mut self, value: ObservableObject) -> Self {
        self.creator_user = Some(value);
        self
    }

    pub fn current_working_directory(mut self, value: String) -> Self {
        self.current_working_directory = Some(value);
        self
    }

    pub fn environment_variables(mut self, value: Dictionary) -> Self {
        self.environment_variables = Some(value);
        self
    }

    pub fn exit_status(mut self, value: i64) -> Self {
        self.exit_status = Some(value);
        self
    }

    pub fn exit_time(mut self, value: String) -> Self {
        self.exit_time = Some(value);
        self
    }

    pub fn is_hidden(mut self, value: bool) -> Self {
        self.is_hidden = Some(value);
        self
    }

    pub fn observable_created_time(mut self, value: String) -> Self {
        self.observable_created_time = Some(value);
        self
    }

    pub fn parent(mut self, value: ObservableObject) -> Self {
        self.parent = Some(value);
        self
    }

    pub fn pid(mut self, value: i64) -> Self {
        self.pid = Some(value);
        self
    }

    pub fn status(mut self, value: String) -> Self {
        self.status = Some(value);
        self
    }

    pub fn build(self) -> ProcessFacet {
        ProcessFacet {
            class_iri: ProcessFacet::CLASS_IRI,
            arguments: self.arguments,
            binary: self.binary,
            creator_user: self.creator_user,
            current_working_directory: self.current_working_directory,
            environment_variables: self.environment_variables,
            exit_status: self.exit_status,
            exit_time: self.exit_time,
            is_hidden: self.is_hidden,
            observable_created_time: self.observable_created_time,
            parent: self.parent,
            pid: self.pid,
            status: self.status,
        }
    }
}

impl CaseObject for ProcessFacet {
    fn class_iri() -> &'static str { ProcessFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ProcessFacet" }
}

/// A process thread is the smallest sequence of programmed instructions that can be managed independently by a scheduler on a computer, which is typically a part of the operating system. It is a componen
#[derive(Debug, Clone, Serialize)]
pub struct ProcessThread {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ProcessThread {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ProcessThread";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ProcessThreadBuilder {
        ProcessThreadBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ProcessThreadBuilder {
}

impl ProcessThreadBuilder {
    pub fn build(self) -> ProcessThread {
        ProcessThread {
            class_iri: ProcessThread::CLASS_IRI,
        }
    }
}

impl CaseObject for ProcessThread {
    fn class_iri() -> &'static str { ProcessThread::CLASS_IRI }
    fn type_name() -> &'static str { "ProcessThread" }
}

/// A profile is an explicit digital representation of identity and characteristics of the owner of a single user account associated with an online service or application. [based on https://en.wikipedia.o
#[derive(Debug, Clone, Serialize)]
pub struct Profile {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Profile {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Profile";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ProfileBuilder {
        ProfileBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ProfileBuilder {
}

impl ProfileBuilder {
    pub fn build(self) -> Profile {
        Profile {
            class_iri: Profile::CLASS_IRI,
        }
    }
}

impl CaseObject for Profile {
    fn class_iri() -> &'static str { Profile::CLASS_IRI }
    fn type_name() -> &'static str { "Profile" }
}

/// A profile facet is a grouping of characteristics unique to an explicit digital representation of identity and characteristics of the owner of a single user account associated with an online service or
#[derive(Debug, Clone, Serialize)]
pub struct ProfileFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:name")]
    pub name: Option<String>,
    #[serde(rename = "uco-observable:contactAddress")]
    pub contact_address: Option<ContactAddress>,
    #[serde(rename = "uco-observable:contactEmail")]
    pub contact_email: Option<ContactEmail>,
    #[serde(rename = "uco-observable:contactMessaging")]
    pub contact_messaging: Option<ContactMessaging>,
    #[serde(rename = "uco-observable:contactPhone")]
    pub contact_phone: Option<ContactPhone>,
    #[serde(rename = "uco-observable:contactURL")]
    pub contact_url: Option<ContactURL>,
    #[serde(rename = "uco-observable:displayName")]
    pub display_name: Option<String>,
    #[serde(rename = "uco-observable:profileAccount")]
    pub profile_account: Option<ObservableObject>,
    #[serde(rename = "uco-observable:profileCreated")]
    pub profile_created: Option<String>,
    #[serde(rename = "uco-observable:profileIdentity")]
    pub profile_identity: Option<Identity>,
    #[serde(rename = "uco-observable:profileLanguage")]
    pub profile_language: Vec<String>,
    #[serde(rename = "uco-observable:profileService")]
    pub profile_service: Option<ObservableObject>,
    #[serde(rename = "uco-observable:profileWebsite")]
    pub profile_website: Option<ObservableObject>,
}

impl ProfileFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ProfileFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ProfileFacetBuilder {
        ProfileFacetBuilder {
            name: None,
            contact_address: None,
            contact_email: None,
            contact_messaging: None,
            contact_phone: None,
            contact_url: None,
            display_name: None,
            profile_account: None,
            profile_created: None,
            profile_identity: None,
            profile_language: Vec::new(),
            profile_service: None,
            profile_website: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ProfileFacetBuilder {
    name: Option<String>,
    contact_address: Option<ContactAddress>,
    contact_email: Option<ContactEmail>,
    contact_messaging: Option<ContactMessaging>,
    contact_phone: Option<ContactPhone>,
    contact_url: Option<ContactURL>,
    display_name: Option<String>,
    profile_account: Option<ObservableObject>,
    profile_created: Option<String>,
    profile_identity: Option<Identity>,
    profile_language: Vec<String>,
    profile_service: Option<ObservableObject>,
    profile_website: Option<ObservableObject>,
}

impl ProfileFacetBuilder {
    pub fn name(mut self, value: String) -> Self {
        self.name = Some(value);
        self
    }

    pub fn contact_address(mut self, value: ContactAddress) -> Self {
        self.contact_address = Some(value);
        self
    }

    pub fn contact_email(mut self, value: ContactEmail) -> Self {
        self.contact_email = Some(value);
        self
    }

    pub fn contact_messaging(mut self, value: ContactMessaging) -> Self {
        self.contact_messaging = Some(value);
        self
    }

    pub fn contact_phone(mut self, value: ContactPhone) -> Self {
        self.contact_phone = Some(value);
        self
    }

    pub fn contact_url(mut self, value: ContactURL) -> Self {
        self.contact_url = Some(value);
        self
    }

    pub fn display_name(mut self, value: String) -> Self {
        self.display_name = Some(value);
        self
    }

    pub fn profile_account(mut self, value: ObservableObject) -> Self {
        self.profile_account = Some(value);
        self
    }

    pub fn profile_created(mut self, value: String) -> Self {
        self.profile_created = Some(value);
        self
    }

    pub fn profile_identity(mut self, value: Identity) -> Self {
        self.profile_identity = Some(value);
        self
    }

    pub fn profile_language(mut self, value: Vec<String>) -> Self {
        self.profile_language = value;
        self
    }

    pub fn profile_service(mut self, value: ObservableObject) -> Self {
        self.profile_service = Some(value);
        self
    }

    pub fn profile_website(mut self, value: ObservableObject) -> Self {
        self.profile_website = Some(value);
        self
    }

    pub fn build(self) -> ProfileFacet {
        ProfileFacet {
            class_iri: ProfileFacet::CLASS_IRI,
            name: self.name,
            contact_address: self.contact_address,
            contact_email: self.contact_email,
            contact_messaging: self.contact_messaging,
            contact_phone: self.contact_phone,
            contact_url: self.contact_url,
            display_name: self.display_name,
            profile_account: self.profile_account,
            profile_created: self.profile_created,
            profile_identity: self.profile_identity,
            profile_language: self.profile_language,
            profile_service: self.profile_service,
            profile_website: self.profile_website,
        }
    }
}

impl CaseObject for ProfileFacet {
    fn class_iri() -> &'static str { ProfileFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ProfileFacet" }
}

/// A properties enumerated effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a characteristic of the observable object is enumerated. An example
#[derive(Debug, Clone, Serialize)]
pub struct PropertiesEnumeratedEffectFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:properties")]
    pub properties: Option<String>,
}

impl PropertiesEnumeratedEffectFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/PropertiesEnumeratedEffectFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> PropertiesEnumeratedEffectFacetBuilder {
        PropertiesEnumeratedEffectFacetBuilder {
            properties: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct PropertiesEnumeratedEffectFacetBuilder {
    properties: Option<String>,
}

impl PropertiesEnumeratedEffectFacetBuilder {
    pub fn properties(mut self, value: String) -> Self {
        self.properties = Some(value);
        self
    }

    pub fn build(self) -> PropertiesEnumeratedEffectFacet {
        PropertiesEnumeratedEffectFacet {
            class_iri: PropertiesEnumeratedEffectFacet::CLASS_IRI,
            properties: self.properties,
        }
    }
}

impl CaseObject for PropertiesEnumeratedEffectFacet {
    fn class_iri() -> &'static str { PropertiesEnumeratedEffectFacet::CLASS_IRI }
    fn type_name() -> &'static str { "PropertiesEnumeratedEffectFacet" }
}

/// A properties read effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a characteristic is read from an observable object. An example of this wo
#[derive(Debug, Clone, Serialize)]
pub struct PropertyReadEffectFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:propertyName")]
    pub property_name: Option<String>,
    #[serde(rename = "uco-observable:value")]
    pub value: Option<String>,
}

impl PropertyReadEffectFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/PropertyReadEffectFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> PropertyReadEffectFacetBuilder {
        PropertyReadEffectFacetBuilder {
            property_name: None,
            value: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct PropertyReadEffectFacetBuilder {
    property_name: Option<String>,
    value: Option<String>,
}

impl PropertyReadEffectFacetBuilder {
    pub fn property_name(mut self, value: String) -> Self {
        self.property_name = Some(value);
        self
    }

    pub fn value(mut self, value: String) -> Self {
        self.value = Some(value);
        self
    }

    pub fn build(self) -> PropertyReadEffectFacet {
        PropertyReadEffectFacet {
            class_iri: PropertyReadEffectFacet::CLASS_IRI,
            property_name: self.property_name,
            value: self.value,
        }
    }
}

impl CaseObject for PropertyReadEffectFacet {
    fn class_iri() -> &'static str { PropertyReadEffectFacet::CLASS_IRI }
    fn type_name() -> &'static str { "PropertyReadEffectFacet" }
}

/// A protocol converter is a device that converts from one protocol to another (e.g. SD to USB, SATA to USB, etc.
#[derive(Debug, Clone, Serialize)]
pub struct ProtocolConverter {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ProtocolConverter {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ProtocolConverter";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ProtocolConverterBuilder {
        ProtocolConverterBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ProtocolConverterBuilder {
}

impl ProtocolConverterBuilder {
    pub fn build(self) -> ProtocolConverter {
        ProtocolConverter {
            class_iri: ProtocolConverter::CLASS_IRI,
        }
    }
}

impl CaseObject for ProtocolConverter {
    fn class_iri() -> &'static str { ProtocolConverter::CLASS_IRI }
    fn type_name() -> &'static str { "ProtocolConverter" }
}

/// A raster picture is a raster (or bitmap) image.
#[derive(Debug, Clone, Serialize)]
pub struct RasterPicture {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl RasterPicture {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/RasterPicture";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> RasterPictureBuilder {
        RasterPictureBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct RasterPictureBuilder {
}

impl RasterPictureBuilder {
    pub fn build(self) -> RasterPicture {
        RasterPicture {
            class_iri: RasterPicture::CLASS_IRI,
        }
    }
}

impl CaseObject for RasterPicture {
    fn class_iri() -> &'static str { RasterPicture::CLASS_IRI }
    fn type_name() -> &'static str { "RasterPicture" }
}

/// A raster picture facet is a grouping of characteristics unique to a raster (or bitmap) image.
#[derive(Debug, Clone, Serialize)]
pub struct RasterPictureFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:bitsPerPixel")]
    pub bits_per_pixel: Option<i64>,
    #[serde(rename = "uco-observable:camera")]
    pub camera: Option<ObservableObject>,
    #[serde(rename = "uco-observable:imageCompressionMethod")]
    pub image_compression_method: Option<String>,
    #[serde(rename = "uco-observable:pictureHeight")]
    pub picture_height: Option<i64>,
    #[serde(rename = "uco-observable:pictureType")]
    pub picture_type: Option<String>,
    #[serde(rename = "uco-observable:pictureWidth")]
    pub picture_width: Option<i64>,
}

impl RasterPictureFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/RasterPictureFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> RasterPictureFacetBuilder {
        RasterPictureFacetBuilder {
            bits_per_pixel: None,
            camera: None,
            image_compression_method: None,
            picture_height: None,
            picture_type: None,
            picture_width: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct RasterPictureFacetBuilder {
    bits_per_pixel: Option<i64>,
    camera: Option<ObservableObject>,
    image_compression_method: Option<String>,
    picture_height: Option<i64>,
    picture_type: Option<String>,
    picture_width: Option<i64>,
}

impl RasterPictureFacetBuilder {
    pub fn bits_per_pixel(mut self, value: i64) -> Self {
        self.bits_per_pixel = Some(value);
        self
    }

    pub fn camera(mut self, value: ObservableObject) -> Self {
        self.camera = Some(value);
        self
    }

    pub fn image_compression_method(mut self, value: String) -> Self {
        self.image_compression_method = Some(value);
        self
    }

    pub fn picture_height(mut self, value: i64) -> Self {
        self.picture_height = Some(value);
        self
    }

    pub fn picture_type(mut self, value: String) -> Self {
        self.picture_type = Some(value);
        self
    }

    pub fn picture_width(mut self, value: i64) -> Self {
        self.picture_width = Some(value);
        self
    }

    pub fn build(self) -> RasterPictureFacet {
        RasterPictureFacet {
            class_iri: RasterPictureFacet::CLASS_IRI,
            bits_per_pixel: self.bits_per_pixel,
            camera: self.camera,
            image_compression_method: self.image_compression_method,
            picture_height: self.picture_height,
            picture_type: self.picture_type,
            picture_width: self.picture_width,
        }
    }
}

impl CaseObject for RasterPictureFacet {
    fn class_iri() -> &'static str { RasterPictureFacet::CLASS_IRI }
    fn type_name() -> &'static str { "RasterPictureFacet" }
}

/// An observable object that was the result of a recovery operation.
#[derive(Debug, Clone, Serialize)]
pub struct RecoveredObject {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl RecoveredObject {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/RecoveredObject";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> RecoveredObjectBuilder {
        RecoveredObjectBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct RecoveredObjectBuilder {
}

impl RecoveredObjectBuilder {
    pub fn build(self) -> RecoveredObject {
        RecoveredObject {
            class_iri: RecoveredObject::CLASS_IRI,
        }
    }
}

impl CaseObject for RecoveredObject {
    fn class_iri() -> &'static str { RecoveredObject::CLASS_IRI }
    fn type_name() -> &'static str { "RecoveredObject" }
}

/// Recoverability status of name, metadata, and content.
#[derive(Debug, Clone, Serialize)]
pub struct RecoveredObjectFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:contentRecoveredStatus")]
    pub content_recovered_status: Vec<String>,
    #[serde(rename = "uco-observable:metadataRecoveredStatus")]
    pub metadata_recovered_status: Vec<String>,
    #[serde(rename = "uco-observable:nameRecoveredStatus")]
    pub name_recovered_status: Vec<String>,
}

impl RecoveredObjectFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/RecoveredObjectFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> RecoveredObjectFacetBuilder {
        RecoveredObjectFacetBuilder {
            content_recovered_status: Vec::new(),
            metadata_recovered_status: Vec::new(),
            name_recovered_status: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct RecoveredObjectFacetBuilder {
    content_recovered_status: Vec<String>,
    metadata_recovered_status: Vec<String>,
    name_recovered_status: Vec<String>,
}

impl RecoveredObjectFacetBuilder {
    pub fn content_recovered_status(mut self, value: Vec<String>) -> Self {
        self.content_recovered_status = value;
        self
    }

    pub fn metadata_recovered_status(mut self, value: Vec<String>) -> Self {
        self.metadata_recovered_status = value;
        self
    }

    pub fn name_recovered_status(mut self, value: Vec<String>) -> Self {
        self.name_recovered_status = value;
        self
    }

    pub fn build(self) -> RecoveredObjectFacet {
        RecoveredObjectFacet {
            class_iri: RecoveredObjectFacet::CLASS_IRI,
            content_recovered_status: self.content_recovered_status,
            metadata_recovered_status: self.metadata_recovered_status,
            name_recovered_status: self.name_recovered_status,
        }
    }
}

impl CaseObject for RecoveredObjectFacet {
    fn class_iri() -> &'static str { RecoveredObjectFacet::CLASS_IRI }
    fn type_name() -> &'static str { "RecoveredObjectFacet" }
}

/// A reparse point is a type of NTFS (New Technology File System) object which is an optional attribute of files and directories meant to define some sort of preprocessing before accessing the said file 
#[derive(Debug, Clone, Serialize)]
pub struct ReparsePoint {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ReparsePoint {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ReparsePoint";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ReparsePointBuilder {
        ReparsePointBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ReparsePointBuilder {
}

impl ReparsePointBuilder {
    pub fn build(self) -> ReparsePoint {
        ReparsePoint {
            class_iri: ReparsePoint::CLASS_IRI,
        }
    }
}

impl CaseObject for ReparsePoint {
    fn class_iri() -> &'static str { ReparsePoint::CLASS_IRI }
    fn type_name() -> &'static str { "ReparsePoint" }
}

/// A SIM card is a subscriber identification module card intended to securely store the international mobile subscriber identity (IMSI) number and its related key, which are used to identify and authenti
#[derive(Debug, Clone, Serialize)]
pub struct SIMCard {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl SIMCard {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/SIMCard";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SIMCardBuilder {
        SIMCardBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SIMCardBuilder {
}

impl SIMCardBuilder {
    pub fn build(self) -> SIMCard {
        SIMCard {
            class_iri: SIMCard::CLASS_IRI,
        }
    }
}

impl CaseObject for SIMCard {
    fn class_iri() -> &'static str { SIMCard::CLASS_IRI }
    fn type_name() -> &'static str { "SIMCard" }
}

/// A SIM card facet is a grouping of characteristics unique to a subscriber identification module card intended to securely store the international mobile subscriber identity (IMSI) number and its relate
#[derive(Debug, Clone, Serialize)]
pub struct SIMCardFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:ICCID")]
    pub iccid: Option<String>,
    #[serde(rename = "uco-observable:IMSI")]
    pub imsi: Option<String>,
    #[serde(rename = "uco-observable:PIN")]
    pub pin: Option<String>,
    #[serde(rename = "uco-observable:PUK")]
    pub puk: Option<String>,
    #[serde(rename = "uco-observable:SIMForm")]
    pub sim_form: Option<String>,
    #[serde(rename = "uco-observable:SIMType")]
    pub sim_type: Option<String>,
    #[serde(rename = "uco-observable:carrier")]
    pub carrier: Option<Identity>,
    #[serde(rename = "uco-observable:storageCapacityInBytes")]
    pub storage_capacity_in_bytes: Option<i64>,
}

impl SIMCardFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/SIMCardFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SIMCardFacetBuilder {
        SIMCardFacetBuilder {
            iccid: None,
            imsi: None,
            pin: None,
            puk: None,
            sim_form: None,
            sim_type: None,
            carrier: None,
            storage_capacity_in_bytes: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SIMCardFacetBuilder {
    iccid: Option<String>,
    imsi: Option<String>,
    pin: Option<String>,
    puk: Option<String>,
    sim_form: Option<String>,
    sim_type: Option<String>,
    carrier: Option<Identity>,
    storage_capacity_in_bytes: Option<i64>,
}

impl SIMCardFacetBuilder {
    pub fn iccid(mut self, value: String) -> Self {
        self.iccid = Some(value);
        self
    }

    pub fn imsi(mut self, value: String) -> Self {
        self.imsi = Some(value);
        self
    }

    pub fn pin(mut self, value: String) -> Self {
        self.pin = Some(value);
        self
    }

    pub fn puk(mut self, value: String) -> Self {
        self.puk = Some(value);
        self
    }

    pub fn sim_form(mut self, value: String) -> Self {
        self.sim_form = Some(value);
        self
    }

    pub fn sim_type(mut self, value: String) -> Self {
        self.sim_type = Some(value);
        self
    }

    pub fn carrier(mut self, value: Identity) -> Self {
        self.carrier = Some(value);
        self
    }

    pub fn storage_capacity_in_bytes(mut self, value: i64) -> Self {
        self.storage_capacity_in_bytes = Some(value);
        self
    }

    pub fn build(self) -> SIMCardFacet {
        SIMCardFacet {
            class_iri: SIMCardFacet::CLASS_IRI,
            iccid: self.iccid,
            imsi: self.imsi,
            pin: self.pin,
            puk: self.puk,
            sim_form: self.sim_form,
            sim_type: self.sim_type,
            carrier: self.carrier,
            storage_capacity_in_bytes: self.storage_capacity_in_bytes,
        }
    }
}

impl CaseObject for SIMCardFacet {
    fn class_iri() -> &'static str { SIMCardFacet::CLASS_IRI }
    fn type_name() -> &'static str { "SIMCardFacet" }
}

/// A SIP address is an identifier for Session Initiation Protocol (SIP) communication.
#[derive(Debug, Clone, Serialize)]
pub struct SIPAddress {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl SIPAddress {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/SIPAddress";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SIPAddressBuilder {
        SIPAddressBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SIPAddressBuilder {
}

impl SIPAddressBuilder {
    pub fn build(self) -> SIPAddress {
        SIPAddress {
            class_iri: SIPAddress::CLASS_IRI,
        }
    }
}

impl CaseObject for SIPAddress {
    fn class_iri() -> &'static str { SIPAddress::CLASS_IRI }
    fn type_name() -> &'static str { "SIPAddress" }
}

/// A SIP address facet is a grouping of characteristics unique to a Session Initiation Protocol (SIP) standards conformant identifier assigned to a user to enable routing and management of SIP standards 
#[derive(Debug, Clone, Serialize)]
pub struct SIPAddressFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl SIPAddressFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/SIPAddressFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SIPAddressFacetBuilder {
        SIPAddressFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SIPAddressFacetBuilder {
}

impl SIPAddressFacetBuilder {
    pub fn build(self) -> SIPAddressFacet {
        SIPAddressFacet {
            class_iri: SIPAddressFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for SIPAddressFacet {
    fn class_iri() -> &'static str { SIPAddressFacet::CLASS_IRI }
    fn type_name() -> &'static str { "SIPAddressFacet" }
}

/// An SMS message is a message conformant to the short message service (SMS) communication protocol standards.
#[derive(Debug, Clone, Serialize)]
pub struct SMSMessage {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl SMSMessage {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/SMSMessage";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SMSMessageBuilder {
        SMSMessageBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SMSMessageBuilder {
}

impl SMSMessageBuilder {
    pub fn build(self) -> SMSMessage {
        SMSMessage {
            class_iri: SMSMessage::CLASS_IRI,
        }
    }
}

impl CaseObject for SMSMessage {
    fn class_iri() -> &'static str { SMSMessage::CLASS_IRI }
    fn type_name() -> &'static str { "SMSMessage" }
}

/// A SMS message facet is a grouping of characteristics unique to a message conformant to the short message service (SMS) communication protocol standards.
#[derive(Debug, Clone, Serialize)]
pub struct SMSMessageFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:isRead")]
    pub is_read: Option<bool>,
}

impl SMSMessageFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/SMSMessageFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SMSMessageFacetBuilder {
        SMSMessageFacetBuilder {
            is_read: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SMSMessageFacetBuilder {
    is_read: Option<bool>,
}

impl SMSMessageFacetBuilder {
    pub fn is_read(mut self, value: bool) -> Self {
        self.is_read = Some(value);
        self
    }

    pub fn build(self) -> SMSMessageFacet {
        SMSMessageFacet {
            class_iri: SMSMessageFacet::CLASS_IRI,
            is_read: self.is_read,
        }
    }
}

impl CaseObject for SMSMessageFacet {
    fn class_iri() -> &'static str { SMSMessageFacet::CLASS_IRI }
    fn type_name() -> &'static str { "SMSMessageFacet" }
}

/// An SQLite blob is a blob (binary large object) of data within an SQLite database. [based on https://en.wikipedia.org/wiki/SQLite]
#[derive(Debug, Clone, Serialize)]
pub struct SQLiteBlob {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl SQLiteBlob {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/SQLiteBlob";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SQLiteBlobBuilder {
        SQLiteBlobBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SQLiteBlobBuilder {
}

impl SQLiteBlobBuilder {
    pub fn build(self) -> SQLiteBlob {
        SQLiteBlob {
            class_iri: SQLiteBlob::CLASS_IRI,
        }
    }
}

impl CaseObject for SQLiteBlob {
    fn class_iri() -> &'static str { SQLiteBlob::CLASS_IRI }
    fn type_name() -> &'static str { "SQLiteBlob" }
}

/// An SQLite blob facet is a grouping of characteristics unique to a blob (binary large object) of data within an SQLite database. [based on https://en.wikipedia.org/wiki/SQLite]
#[derive(Debug, Clone, Serialize)]
pub struct SQLiteBlobFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:columnName")]
    pub column_name: Option<String>,
    #[serde(rename = "uco-observable:rowCondition")]
    pub row_condition: Option<String>,
    #[serde(rename = "uco-observable:rowIndex")]
    pub row_index: Vec<u64>,
    #[serde(rename = "uco-observable:tableName")]
    pub table_name: Option<String>,
}

impl SQLiteBlobFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/SQLiteBlobFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SQLiteBlobFacetBuilder {
        SQLiteBlobFacetBuilder {
            column_name: None,
            row_condition: None,
            row_index: Vec::new(),
            table_name: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SQLiteBlobFacetBuilder {
    column_name: Option<String>,
    row_condition: Option<String>,
    row_index: Vec<u64>,
    table_name: Option<String>,
}

impl SQLiteBlobFacetBuilder {
    pub fn column_name(mut self, value: String) -> Self {
        self.column_name = Some(value);
        self
    }

    pub fn row_condition(mut self, value: String) -> Self {
        self.row_condition = Some(value);
        self
    }

    pub fn row_index(mut self, value: Vec<u64>) -> Self {
        self.row_index = value;
        self
    }

    pub fn table_name(mut self, value: String) -> Self {
        self.table_name = Some(value);
        self
    }

    pub fn build(self) -> SQLiteBlobFacet {
        SQLiteBlobFacet {
            class_iri: SQLiteBlobFacet::CLASS_IRI,
            column_name: self.column_name,
            row_condition: self.row_condition,
            row_index: self.row_index,
            table_name: self.table_name,
        }
    }
}

impl CaseObject for SQLiteBlobFacet {
    fn class_iri() -> &'static str { SQLiteBlobFacet::CLASS_IRI }
    fn type_name() -> &'static str { "SQLiteBlobFacet" }
}

/// A security appliance is a purpose-built computer with software or firmware that is designed to provide a specific security function to protect computer networks.
#[derive(Debug, Clone, Serialize)]
pub struct SecurityAppliance {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl SecurityAppliance {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/SecurityAppliance";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SecurityApplianceBuilder {
        SecurityApplianceBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SecurityApplianceBuilder {
}

impl SecurityApplianceBuilder {
    pub fn build(self) -> SecurityAppliance {
        SecurityAppliance {
            class_iri: SecurityAppliance::CLASS_IRI,
        }
    }
}

impl CaseObject for SecurityAppliance {
    fn class_iri() -> &'static str { SecurityAppliance::CLASS_IRI }
    fn type_name() -> &'static str { "SecurityAppliance" }
}

/// A semaphore is a variable or abstract data type used to control access to a common resource by multiple processes and avoid critical section problems in a concurrent system such as a multitasking oper
#[derive(Debug, Clone, Serialize)]
pub struct Semaphore {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Semaphore {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Semaphore";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SemaphoreBuilder {
        SemaphoreBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SemaphoreBuilder {
}

impl SemaphoreBuilder {
    pub fn build(self) -> Semaphore {
        Semaphore {
            class_iri: Semaphore::CLASS_IRI,
        }
    }
}

impl CaseObject for Semaphore {
    fn class_iri() -> &'static str { Semaphore::CLASS_IRI }
    fn type_name() -> &'static str { "Semaphore" }
}

/// A send control code effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a control code, or other control-oriented communication signal, is sent
#[derive(Debug, Clone, Serialize)]
pub struct SendControlCodeEffectFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:controlCode")]
    pub control_code: Option<String>,
}

impl SendControlCodeEffectFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/SendControlCodeEffectFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SendControlCodeEffectFacetBuilder {
        SendControlCodeEffectFacetBuilder {
            control_code: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SendControlCodeEffectFacetBuilder {
    control_code: Option<String>,
}

impl SendControlCodeEffectFacetBuilder {
    pub fn control_code(mut self, value: String) -> Self {
        self.control_code = Some(value);
        self
    }

    pub fn build(self) -> SendControlCodeEffectFacet {
        SendControlCodeEffectFacet {
            class_iri: SendControlCodeEffectFacet::CLASS_IRI,
            control_code: self.control_code,
        }
    }
}

impl CaseObject for SendControlCodeEffectFacet {
    fn class_iri() -> &'static str { SendControlCodeEffectFacet::CLASS_IRI }
    fn type_name() -> &'static str { "SendControlCodeEffectFacet" }
}

/// A server is a server rack-mount based computer, minicomputer, supercomputer, etc.
#[derive(Debug, Clone, Serialize)]
pub struct Server {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Server {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Server";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ServerBuilder {
        ServerBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ServerBuilder {
}

impl ServerBuilder {
    pub fn build(self) -> Server {
        Server {
            class_iri: Server::CLASS_IRI,
        }
    }
}

impl CaseObject for Server {
    fn class_iri() -> &'static str { Server::CLASS_IRI }
    fn type_name() -> &'static str { "Server" }
}

/// A shop listing is a listing of offered products on an online marketplace/shop.
#[derive(Debug, Clone, Serialize)]
pub struct ShopListing {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl ShopListing {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ShopListing";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ShopListingBuilder {
        ShopListingBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ShopListingBuilder {
}

impl ShopListingBuilder {
    pub fn build(self) -> ShopListing {
        ShopListing {
            class_iri: ShopListing::CLASS_IRI,
        }
    }
}

impl CaseObject for ShopListing {
    fn class_iri() -> &'static str { ShopListing::CLASS_IRI }
    fn type_name() -> &'static str { "ShopListing" }
}

/// A smart device is a microprocessor IoT device that is expected to be connected directly to cloud-based networks or via smartphone
#[derive(Debug, Clone, Serialize)]
pub struct SmartDevice {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl SmartDevice {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/SmartDevice";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SmartDeviceBuilder {
        SmartDeviceBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SmartDeviceBuilder {
}

impl SmartDeviceBuilder {
    pub fn build(self) -> SmartDevice {
        SmartDevice {
            class_iri: SmartDevice::CLASS_IRI,
        }
    }
}

impl CaseObject for SmartDevice {
    fn class_iri() -> &'static str { SmartDevice::CLASS_IRI }
    fn type_name() -> &'static str { "SmartDevice" }
}

/// A smartphone is a portable device that combines mobile telephone and computing functions into one unit.  Examples include iPhone, Samsung Galaxy, Huawei, Blackberry. (Inferred by model and OperatingSy
#[derive(Debug, Clone, Serialize)]
pub struct SmartPhone {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl SmartPhone {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/SmartPhone";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SmartPhoneBuilder {
        SmartPhoneBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SmartPhoneBuilder {
}

impl SmartPhoneBuilder {
    pub fn build(self) -> SmartPhone {
        SmartPhone {
            class_iri: SmartPhone::CLASS_IRI,
        }
    }
}

impl CaseObject for SmartPhone {
    fn class_iri() -> &'static str { SmartPhone::CLASS_IRI }
    fn type_name() -> &'static str { "SmartPhone" }
}

/// A snapshot is a file system object representing a snapshot of the contents of a part of a file system at a point in time.
#[derive(Debug, Clone, Serialize)]
pub struct Snapshot {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Snapshot {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Snapshot";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SnapshotBuilder {
        SnapshotBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SnapshotBuilder {
}

impl SnapshotBuilder {
    pub fn build(self) -> Snapshot {
        Snapshot {
            class_iri: Snapshot::CLASS_IRI,
        }
    }
}

impl CaseObject for Snapshot {
    fn class_iri() -> &'static str { Snapshot::CLASS_IRI }
    fn type_name() -> &'static str { "Snapshot" }
}

/// A socket is a special file used for inter-process communication, which enables communication between two processes. In addition to sending data, processes can send file descriptors across a Unix domai
#[derive(Debug, Clone, Serialize)]
pub struct Socket {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Socket {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Socket";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SocketBuilder {
        SocketBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SocketBuilder {
}

impl SocketBuilder {
    pub fn build(self) -> Socket {
        Socket {
            class_iri: Socket::CLASS_IRI,
        }
    }
}

impl CaseObject for Socket {
    fn class_iri() -> &'static str { Socket::CLASS_IRI }
    fn type_name() -> &'static str { "Socket" }
}

/// A socket address (combining and IP address and a port number) is a composite identifier for a network socket endpoint supporting internet protocol communications.
#[derive(Debug, Clone, Serialize)]
pub struct SocketAddress {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl SocketAddress {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/SocketAddress";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SocketAddressBuilder {
        SocketAddressBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SocketAddressBuilder {
}

impl SocketAddressBuilder {
    pub fn build(self) -> SocketAddress {
        SocketAddress {
            class_iri: SocketAddress::CLASS_IRI,
        }
    }
}

impl CaseObject for SocketAddress {
    fn class_iri() -> &'static str { SocketAddress::CLASS_IRI }
    fn type_name() -> &'static str { "SocketAddress" }
}

/// Software is a definitely scoped instance of a collection of data or computer instructions that tell the computer how to work. [based on https://en.wikipedia.org/wiki/Software]
#[derive(Debug, Clone, Serialize)]
pub struct Software {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Software {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Software";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SoftwareBuilder {
        SoftwareBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SoftwareBuilder {
}

impl SoftwareBuilder {
    pub fn build(self) -> Software {
        Software {
            class_iri: Software::CLASS_IRI,
        }
    }
}

impl CaseObject for Software {
    fn class_iri() -> &'static str { Software::CLASS_IRI }
    fn type_name() -> &'static str { "Software" }
}

/// A software facet is a grouping of characteristics unique to a software program (a definitively scoped instance of a collection of data or computer instructions that tell the computer how to work). [ba
#[derive(Debug, Clone, Serialize)]
pub struct SoftwareFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:cpeid")]
    pub cpeid: Option<String>,
    #[serde(rename = "uco-observable:language")]
    pub language: Option<String>,
    #[serde(rename = "uco-observable:manufacturer")]
    pub manufacturer: Option<Identity>,
    #[serde(rename = "uco-observable:swid")]
    pub swid: Option<String>,
    #[serde(rename = "uco-observable:version")]
    pub version: Option<String>,
}

impl SoftwareFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/SoftwareFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SoftwareFacetBuilder {
        SoftwareFacetBuilder {
            cpeid: None,
            language: None,
            manufacturer: None,
            swid: None,
            version: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SoftwareFacetBuilder {
    cpeid: Option<String>,
    language: Option<String>,
    manufacturer: Option<Identity>,
    swid: Option<String>,
    version: Option<String>,
}

impl SoftwareFacetBuilder {
    pub fn cpeid(mut self, value: String) -> Self {
        self.cpeid = Some(value);
        self
    }

    pub fn language(mut self, value: String) -> Self {
        self.language = Some(value);
        self
    }

    pub fn manufacturer(mut self, value: Identity) -> Self {
        self.manufacturer = Some(value);
        self
    }

    pub fn swid(mut self, value: String) -> Self {
        self.swid = Some(value);
        self
    }

    pub fn version(mut self, value: String) -> Self {
        self.version = Some(value);
        self
    }

    pub fn build(self) -> SoftwareFacet {
        SoftwareFacet {
            class_iri: SoftwareFacet::CLASS_IRI,
            cpeid: self.cpeid,
            language: self.language,
            manufacturer: self.manufacturer,
            swid: self.swid,
            version: self.version,
        }
    }
}

impl CaseObject for SoftwareFacet {
    fn class_iri() -> &'static str { SoftwareFacet::CLASS_IRI }
    fn type_name() -> &'static str { "SoftwareFacet" }
}

/// A state change effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a state of the observable object is changed.
#[derive(Debug, Clone, Serialize)]
pub struct StateChangeEffectFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:newObject")]
    pub new_object: Option<ObservableObject>,
    #[serde(rename = "uco-observable:oldObject")]
    pub old_object: Option<ObservableObject>,
}

impl StateChangeEffectFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/StateChangeEffectFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> StateChangeEffectFacetBuilder {
        StateChangeEffectFacetBuilder {
            new_object: None,
            old_object: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct StateChangeEffectFacetBuilder {
    new_object: Option<ObservableObject>,
    old_object: Option<ObservableObject>,
}

impl StateChangeEffectFacetBuilder {
    pub fn new_object(mut self, value: ObservableObject) -> Self {
        self.new_object = Some(value);
        self
    }

    pub fn old_object(mut self, value: ObservableObject) -> Self {
        self.old_object = Some(value);
        self
    }

    pub fn build(self) -> StateChangeEffectFacet {
        StateChangeEffectFacet {
            class_iri: StateChangeEffectFacet::CLASS_IRI,
            new_object: self.new_object,
            old_object: self.old_object,
        }
    }
}

impl CaseObject for StateChangeEffectFacet {
    fn class_iri() -> &'static str { StateChangeEffectFacet::CLASS_IRI }
    fn type_name() -> &'static str { "StateChangeEffectFacet" }
}

/// A storage medium is any digital storage device that applies electromagnetic or optical surfaces, or depends solely on electronic circuits as solid state storage, for storing digital data. Examples inc
#[derive(Debug, Clone, Serialize)]
pub struct StorageMedium {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl StorageMedium {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/StorageMedium";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> StorageMediumBuilder {
        StorageMediumBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct StorageMediumBuilder {
}

impl StorageMediumBuilder {
    pub fn build(self) -> StorageMedium {
        StorageMedium {
            class_iri: StorageMedium::CLASS_IRI,
        }
    }
}

impl CaseObject for StorageMedium {
    fn class_iri() -> &'static str { StorageMedium::CLASS_IRI }
    fn type_name() -> &'static str { "StorageMedium" }
}

/// A storage medium facet is a grouping of characteristics unique to a the storage capabilities of a piece of equipment or a mechanism designed to serve a special purpose or perform a special function.
#[derive(Debug, Clone, Serialize)]
pub struct StorageMediumFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:totalStorageCapacityInBytes")]
    pub total_storage_capacity_in_bytes: Option<i64>,
}

impl StorageMediumFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/StorageMediumFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> StorageMediumFacetBuilder {
        StorageMediumFacetBuilder {
            total_storage_capacity_in_bytes: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct StorageMediumFacetBuilder {
    total_storage_capacity_in_bytes: Option<i64>,
}

impl StorageMediumFacetBuilder {
    pub fn total_storage_capacity_in_bytes(mut self, value: i64) -> Self {
        self.total_storage_capacity_in_bytes = Some(value);
        self
    }

    pub fn build(self) -> StorageMediumFacet {
        StorageMediumFacet {
            class_iri: StorageMediumFacet::CLASS_IRI,
            total_storage_capacity_in_bytes: self.total_storage_capacity_in_bytes,
        }
    }
}

impl CaseObject for StorageMediumFacet {
    fn class_iri() -> &'static str { StorageMediumFacet::CLASS_IRI }
    fn type_name() -> &'static str { "StorageMediumFacet" }
}

/// A symbolic link is a file that contains a reference to another file or directory in the form of an absolute or relative path and that affects pathname resolution. [based on https://en.wikipedia.org/wi
#[derive(Debug, Clone, Serialize)]
pub struct SymbolicLink {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl SymbolicLink {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/SymbolicLink";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SymbolicLinkBuilder {
        SymbolicLinkBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SymbolicLinkBuilder {
}

impl SymbolicLinkBuilder {
    pub fn build(self) -> SymbolicLink {
        SymbolicLink {
            class_iri: SymbolicLink::CLASS_IRI,
        }
    }
}

impl CaseObject for SymbolicLink {
    fn class_iri() -> &'static str { SymbolicLink::CLASS_IRI }
    fn type_name() -> &'static str { "SymbolicLink" }
}

/// A symbolic link facet is a grouping of characteristics unique to a file that contains a reference to another file or directory in the form of an absolute or relative path and that affects pathname res
#[derive(Debug, Clone, Serialize)]
pub struct SymbolicLinkFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:targetFile")]
    pub target_file: Option<ObservableObject>,
}

impl SymbolicLinkFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/SymbolicLinkFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> SymbolicLinkFacetBuilder {
        SymbolicLinkFacetBuilder {
            target_file: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct SymbolicLinkFacetBuilder {
    target_file: Option<ObservableObject>,
}

impl SymbolicLinkFacetBuilder {
    pub fn target_file(mut self, value: ObservableObject) -> Self {
        self.target_file = Some(value);
        self
    }

    pub fn build(self) -> SymbolicLinkFacet {
        SymbolicLinkFacet {
            class_iri: SymbolicLinkFacet::CLASS_IRI,
            target_file: self.target_file,
        }
    }
}

impl CaseObject for SymbolicLinkFacet {
    fn class_iri() -> &'static str { SymbolicLinkFacet::CLASS_IRI }
    fn type_name() -> &'static str { "SymbolicLinkFacet" }
}

/// A TCP connection is a network connection that is conformant to the Transfer 
#[derive(Debug, Clone, Serialize)]
pub struct TCPConnection {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl TCPConnection {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/TCPConnection";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> TCPConnectionBuilder {
        TCPConnectionBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct TCPConnectionBuilder {
}

impl TCPConnectionBuilder {
    pub fn build(self) -> TCPConnection {
        TCPConnection {
            class_iri: TCPConnection::CLASS_IRI,
        }
    }
}

impl CaseObject for TCPConnection {
    fn class_iri() -> &'static str { TCPConnection::CLASS_IRI }
    fn type_name() -> &'static str { "TCPConnection" }
}

/// A TCP connection facet is a grouping of characteristics unique to portions of a network connection that are conformant to the Transmission Control Protocl (TCP) standard.
#[derive(Debug, Clone, Serialize)]
pub struct TCPConnectionFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:destinationFlags")]
    pub destination_flags: Vec<Vec<u8>>,
    #[serde(rename = "uco-observable:sourceFlags")]
    pub source_flags: Vec<Vec<u8>>,
}

impl TCPConnectionFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/TCPConnectionFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> TCPConnectionFacetBuilder {
        TCPConnectionFacetBuilder {
            destination_flags: Vec::new(),
            source_flags: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct TCPConnectionFacetBuilder {
    destination_flags: Vec<Vec<u8>>,
    source_flags: Vec<Vec<u8>>,
}

impl TCPConnectionFacetBuilder {
    pub fn destination_flags(mut self, value: Vec<Vec<u8>>) -> Self {
        self.destination_flags = value;
        self
    }

    pub fn source_flags(mut self, value: Vec<Vec<u8>>) -> Self {
        self.source_flags = value;
        self
    }

    pub fn build(self) -> TCPConnectionFacet {
        TCPConnectionFacet {
            class_iri: TCPConnectionFacet::CLASS_IRI,
            destination_flags: self.destination_flags,
            source_flags: self.source_flags,
        }
    }
}

impl CaseObject for TCPConnectionFacet {
    fn class_iri() -> &'static str { TCPConnectionFacet::CLASS_IRI }
    fn type_name() -> &'static str { "TCPConnectionFacet" }
}

/// A database table field and its associated value contained within a relational database.
#[derive(Debug, Clone, Serialize)]
pub struct TableField {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl TableField {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/TableField";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> TableFieldBuilder {
        TableFieldBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct TableFieldBuilder {
}

impl TableFieldBuilder {
    pub fn build(self) -> TableField {
        TableField {
            class_iri: TableField::CLASS_IRI,
        }
    }
}

impl CaseObject for TableField {
    fn class_iri() -> &'static str { TableField::CLASS_IRI }
    fn type_name() -> &'static str { "TableField" }
}

/// A database record facet contains properties associated with a specific table record value from a database.
#[derive(Debug, Clone, Serialize)]
pub struct TableFieldFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:recordFieldIsNull")]
    pub record_field_is_null: Option<bool>,
    #[serde(rename = "uco-observable:recordFieldName")]
    pub record_field_name: Option<String>,
    #[serde(rename = "uco-observable:recordFieldValue")]
    pub record_field_value: Option<serde_json::Value>,
    #[serde(rename = "uco-observable:recordRowID")]
    pub record_row_id: Option<serde_json::Value>,
    #[serde(rename = "uco-observable:tableName")]
    pub table_name: Option<String>,
    #[serde(rename = "uco-observable:tableSchema")]
    pub table_schema: Option<String>,
}

impl TableFieldFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/TableFieldFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> TableFieldFacetBuilder {
        TableFieldFacetBuilder {
            record_field_is_null: None,
            record_field_name: None,
            record_field_value: None,
            record_row_id: None,
            table_name: None,
            table_schema: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct TableFieldFacetBuilder {
    record_field_is_null: Option<bool>,
    record_field_name: Option<String>,
    record_field_value: Option<serde_json::Value>,
    record_row_id: Option<serde_json::Value>,
    table_name: Option<String>,
    table_schema: Option<String>,
}

impl TableFieldFacetBuilder {
    pub fn record_field_is_null(mut self, value: bool) -> Self {
        self.record_field_is_null = Some(value);
        self
    }

    pub fn record_field_name(mut self, value: String) -> Self {
        self.record_field_name = Some(value);
        self
    }

    pub fn record_field_value(mut self, value: serde_json::Value) -> Self {
        self.record_field_value = Some(value);
        self
    }

    pub fn record_row_id(mut self, value: serde_json::Value) -> Self {
        self.record_row_id = Some(value);
        self
    }

    pub fn table_name(mut self, value: String) -> Self {
        self.table_name = Some(value);
        self
    }

    pub fn table_schema(mut self, value: String) -> Self {
        self.table_schema = Some(value);
        self
    }

    pub fn build(self) -> TableFieldFacet {
        TableFieldFacet {
            class_iri: TableFieldFacet::CLASS_IRI,
            record_field_is_null: self.record_field_is_null,
            record_field_name: self.record_field_name,
            record_field_value: self.record_field_value,
            record_row_id: self.record_row_id,
            table_name: self.table_name,
            table_schema: self.table_schema,
        }
    }
}

impl CaseObject for TableFieldFacet {
    fn class_iri() -> &'static str { TableFieldFacet::CLASS_IRI }
    fn type_name() -> &'static str { "TableFieldFacet" }
}

/// A tablet is a mobile computer that is primarily operated by touching the screen. (Devices categorized by their manufacturer as a Tablet)
#[derive(Debug, Clone, Serialize)]
pub struct Tablet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Tablet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Tablet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> TabletBuilder {
        TabletBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct TabletBuilder {
}

impl TabletBuilder {
    pub fn build(self) -> Tablet {
        Tablet {
            class_iri: Tablet::CLASS_IRI,
        }
    }
}

impl CaseObject for Tablet {
    fn class_iri() -> &'static str { Tablet::CLASS_IRI }
    fn type_name() -> &'static str { "Tablet" }
}

/// A task action type is a grouping of characteristics for a scheduled action to be completed.
#[derive(Debug, Clone, Serialize)]
pub struct TaskActionType {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:actionID")]
    pub action_id: Option<String>,
    #[serde(rename = "uco-observable:actionType")]
    pub action_type: Vec<String>,
    #[serde(rename = "uco-observable:iComHandlerAction")]
    pub i_com_handler_action: Option<IComHandlerActionType>,
    #[serde(rename = "uco-observable:iEmailAction")]
    pub i_email_action: Option<ObservableObject>,
    #[serde(rename = "uco-observable:iExecAction")]
    pub i_exec_action: Option<IExecActionType>,
    #[serde(rename = "uco-observable:iShowMessageAction")]
    pub i_show_message_action: Option<IShowMessageActionType>,
}

impl TaskActionType {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/TaskActionType";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> TaskActionTypeBuilder {
        TaskActionTypeBuilder {
            action_id: None,
            action_type: Vec::new(),
            i_com_handler_action: None,
            i_email_action: None,
            i_exec_action: None,
            i_show_message_action: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct TaskActionTypeBuilder {
    action_id: Option<String>,
    action_type: Vec<String>,
    i_com_handler_action: Option<IComHandlerActionType>,
    i_email_action: Option<ObservableObject>,
    i_exec_action: Option<IExecActionType>,
    i_show_message_action: Option<IShowMessageActionType>,
}

impl TaskActionTypeBuilder {
    pub fn action_id(mut self, value: String) -> Self {
        self.action_id = Some(value);
        self
    }

    pub fn action_type(mut self, value: Vec<String>) -> Self {
        self.action_type = value;
        self
    }

    pub fn i_com_handler_action(mut self, value: IComHandlerActionType) -> Self {
        self.i_com_handler_action = Some(value);
        self
    }

    pub fn i_email_action(mut self, value: ObservableObject) -> Self {
        self.i_email_action = Some(value);
        self
    }

    pub fn i_exec_action(mut self, value: IExecActionType) -> Self {
        self.i_exec_action = Some(value);
        self
    }

    pub fn i_show_message_action(mut self, value: IShowMessageActionType) -> Self {
        self.i_show_message_action = Some(value);
        self
    }

    pub fn build(self) -> TaskActionType {
        TaskActionType {
            class_iri: TaskActionType::CLASS_IRI,
            action_id: self.action_id,
            action_type: self.action_type,
            i_com_handler_action: self.i_com_handler_action,
            i_email_action: self.i_email_action,
            i_exec_action: self.i_exec_action,
            i_show_message_action: self.i_show_message_action,
        }
    }
}

impl CaseObject for TaskActionType {
    fn class_iri() -> &'static str { TaskActionType::CLASS_IRI }
    fn type_name() -> &'static str { "TaskActionType" }
}

/// A trigger type is a grouping of characterizes unique to a set of criteria that, when met, starts the execution of a task within a Windows operating system. [based on https://docs.microsoft.com/en-us/w
#[derive(Debug, Clone, Serialize)]
pub struct TriggerType {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:isEnabled")]
    pub is_enabled: Option<bool>,
    #[serde(rename = "uco-observable:triggerBeginTime")]
    pub trigger_begin_time: Option<String>,
    #[serde(rename = "uco-observable:triggerDelay")]
    pub trigger_delay: Option<String>,
    #[serde(rename = "uco-observable:triggerEndTime")]
    pub trigger_end_time: Option<String>,
    #[serde(rename = "uco-observable:triggerFrequency")]
    pub trigger_frequency: Vec<String>,
    #[serde(rename = "uco-observable:triggerMaxRunTime")]
    pub trigger_max_run_time: Option<String>,
    #[serde(rename = "uco-observable:triggerSessionChangeType")]
    pub trigger_session_change_type: Option<String>,
    #[serde(rename = "uco-observable:triggerType")]
    pub trigger_type: Vec<String>,
}

impl TriggerType {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/TriggerType";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> TriggerTypeBuilder {
        TriggerTypeBuilder {
            is_enabled: None,
            trigger_begin_time: None,
            trigger_delay: None,
            trigger_end_time: None,
            trigger_frequency: Vec::new(),
            trigger_max_run_time: None,
            trigger_session_change_type: None,
            trigger_type: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct TriggerTypeBuilder {
    is_enabled: Option<bool>,
    trigger_begin_time: Option<String>,
    trigger_delay: Option<String>,
    trigger_end_time: Option<String>,
    trigger_frequency: Vec<String>,
    trigger_max_run_time: Option<String>,
    trigger_session_change_type: Option<String>,
    trigger_type: Vec<String>,
}

impl TriggerTypeBuilder {
    pub fn is_enabled(mut self, value: bool) -> Self {
        self.is_enabled = Some(value);
        self
    }

    pub fn trigger_begin_time(mut self, value: String) -> Self {
        self.trigger_begin_time = Some(value);
        self
    }

    pub fn trigger_delay(mut self, value: String) -> Self {
        self.trigger_delay = Some(value);
        self
    }

    pub fn trigger_end_time(mut self, value: String) -> Self {
        self.trigger_end_time = Some(value);
        self
    }

    pub fn trigger_frequency(mut self, value: Vec<String>) -> Self {
        self.trigger_frequency = value;
        self
    }

    pub fn trigger_max_run_time(mut self, value: String) -> Self {
        self.trigger_max_run_time = Some(value);
        self
    }

    pub fn trigger_session_change_type(mut self, value: String) -> Self {
        self.trigger_session_change_type = Some(value);
        self
    }

    pub fn trigger_type(mut self, value: Vec<String>) -> Self {
        self.trigger_type = value;
        self
    }

    pub fn build(self) -> TriggerType {
        TriggerType {
            class_iri: TriggerType::CLASS_IRI,
            is_enabled: self.is_enabled,
            trigger_begin_time: self.trigger_begin_time,
            trigger_delay: self.trigger_delay,
            trigger_end_time: self.trigger_end_time,
            trigger_frequency: self.trigger_frequency,
            trigger_max_run_time: self.trigger_max_run_time,
            trigger_session_change_type: self.trigger_session_change_type,
            trigger_type: self.trigger_type,
        }
    }
}

impl CaseObject for TriggerType {
    fn class_iri() -> &'static str { TriggerType::CLASS_IRI }
    fn type_name() -> &'static str { "TriggerType" }
}

/// A tweet is message submitted by a Twitter user account to the Twitter microblogging platform.
#[derive(Debug, Clone, Serialize)]
pub struct Tweet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Tweet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Tweet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> TweetBuilder {
        TweetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct TweetBuilder {
}

impl TweetBuilder {
    pub fn build(self) -> Tweet {
        Tweet {
            class_iri: Tweet::CLASS_IRI,
        }
    }
}

impl CaseObject for Tweet {
    fn class_iri() -> &'static str { Tweet::CLASS_IRI }
    fn type_name() -> &'static str { "Tweet" }
}

/// A twitter profile facet is a grouping of characteristics unique to an explicit digital representation of identity and characteristics of the owner of a single Twitter user account. [based on https://e
#[derive(Debug, Clone, Serialize)]
pub struct TwitterProfileFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:favoritesCount")]
    pub favorites_count: Option<u64>,
    #[serde(rename = "uco-observable:followersCount")]
    pub followers_count: Option<u64>,
    #[serde(rename = "uco-observable:friendsCount")]
    pub friends_count: Option<u64>,
    #[serde(rename = "uco-observable:listedCount")]
    pub listed_count: Option<i64>,
    #[serde(rename = "uco-observable:profileBackgroundHash")]
    pub profile_background_hash: Vec<Hash>,
    #[serde(rename = "uco-observable:profileBackgroundLocation")]
    pub profile_background_location: Option<ObservableObject>,
    #[serde(rename = "uco-observable:profileBannerHash")]
    pub profile_banner_hash: Vec<Hash>,
    #[serde(rename = "uco-observable:profileBannerLocation")]
    pub profile_banner_location: Option<ObservableObject>,
    #[serde(rename = "uco-observable:profileImageHash")]
    pub profile_image_hash: Vec<Hash>,
    #[serde(rename = "uco-observable:profileImageLocation")]
    pub profile_image_location: Option<ObservableObject>,
    #[serde(rename = "uco-observable:profileIsProtected")]
    pub profile_is_protected: Option<bool>,
    #[serde(rename = "uco-observable:profileIsVerified")]
    pub profile_is_verified: Option<bool>,
    #[serde(rename = "uco-observable:statusesCount")]
    pub statuses_count: Option<u64>,
    #[serde(rename = "uco-observable:twitterHandle")]
    pub twitter_handle: Option<String>,
    #[serde(rename = "uco-observable:twitterId")]
    pub twitter_id: Option<String>,
    #[serde(rename = "uco-observable:userLocationString")]
    pub user_location_string: Option<String>,
}

impl TwitterProfileFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/TwitterProfileFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> TwitterProfileFacetBuilder {
        TwitterProfileFacetBuilder {
            favorites_count: None,
            followers_count: None,
            friends_count: None,
            listed_count: None,
            profile_background_hash: Vec::new(),
            profile_background_location: None,
            profile_banner_hash: Vec::new(),
            profile_banner_location: None,
            profile_image_hash: Vec::new(),
            profile_image_location: None,
            profile_is_protected: None,
            profile_is_verified: None,
            statuses_count: None,
            twitter_handle: None,
            twitter_id: None,
            user_location_string: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct TwitterProfileFacetBuilder {
    favorites_count: Option<u64>,
    followers_count: Option<u64>,
    friends_count: Option<u64>,
    listed_count: Option<i64>,
    profile_background_hash: Vec<Hash>,
    profile_background_location: Option<ObservableObject>,
    profile_banner_hash: Vec<Hash>,
    profile_banner_location: Option<ObservableObject>,
    profile_image_hash: Vec<Hash>,
    profile_image_location: Option<ObservableObject>,
    profile_is_protected: Option<bool>,
    profile_is_verified: Option<bool>,
    statuses_count: Option<u64>,
    twitter_handle: Option<String>,
    twitter_id: Option<String>,
    user_location_string: Option<String>,
}

impl TwitterProfileFacetBuilder {
    pub fn favorites_count(mut self, value: u64) -> Self {
        self.favorites_count = Some(value);
        self
    }

    pub fn followers_count(mut self, value: u64) -> Self {
        self.followers_count = Some(value);
        self
    }

    pub fn friends_count(mut self, value: u64) -> Self {
        self.friends_count = Some(value);
        self
    }

    pub fn listed_count(mut self, value: i64) -> Self {
        self.listed_count = Some(value);
        self
    }

    pub fn profile_background_hash(mut self, value: Vec<Hash>) -> Self {
        self.profile_background_hash = value;
        self
    }

    pub fn profile_background_location(mut self, value: ObservableObject) -> Self {
        self.profile_background_location = Some(value);
        self
    }

    pub fn profile_banner_hash(mut self, value: Vec<Hash>) -> Self {
        self.profile_banner_hash = value;
        self
    }

    pub fn profile_banner_location(mut self, value: ObservableObject) -> Self {
        self.profile_banner_location = Some(value);
        self
    }

    pub fn profile_image_hash(mut self, value: Vec<Hash>) -> Self {
        self.profile_image_hash = value;
        self
    }

    pub fn profile_image_location(mut self, value: ObservableObject) -> Self {
        self.profile_image_location = Some(value);
        self
    }

    pub fn profile_is_protected(mut self, value: bool) -> Self {
        self.profile_is_protected = Some(value);
        self
    }

    pub fn profile_is_verified(mut self, value: bool) -> Self {
        self.profile_is_verified = Some(value);
        self
    }

    pub fn statuses_count(mut self, value: u64) -> Self {
        self.statuses_count = Some(value);
        self
    }

    pub fn twitter_handle(mut self, value: String) -> Self {
        self.twitter_handle = Some(value);
        self
    }

    pub fn twitter_id(mut self, value: String) -> Self {
        self.twitter_id = Some(value);
        self
    }

    pub fn user_location_string(mut self, value: String) -> Self {
        self.user_location_string = Some(value);
        self
    }

    pub fn build(self) -> TwitterProfileFacet {
        TwitterProfileFacet {
            class_iri: TwitterProfileFacet::CLASS_IRI,
            favorites_count: self.favorites_count,
            followers_count: self.followers_count,
            friends_count: self.friends_count,
            listed_count: self.listed_count,
            profile_background_hash: self.profile_background_hash,
            profile_background_location: self.profile_background_location,
            profile_banner_hash: self.profile_banner_hash,
            profile_banner_location: self.profile_banner_location,
            profile_image_hash: self.profile_image_hash,
            profile_image_location: self.profile_image_location,
            profile_is_protected: self.profile_is_protected,
            profile_is_verified: self.profile_is_verified,
            statuses_count: self.statuses_count,
            twitter_handle: self.twitter_handle,
            twitter_id: self.twitter_id,
            user_location_string: self.user_location_string,
        }
    }
}

impl CaseObject for TwitterProfileFacet {
    fn class_iri() -> &'static str { TwitterProfileFacet::CLASS_IRI }
    fn type_name() -> &'static str { "TwitterProfileFacet" }
}

/// A UNIX account is an account on a UNIX operating system.
#[derive(Debug, Clone, Serialize)]
pub struct UNIXAccount {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl UNIXAccount {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXAccount";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> UNIXAccountBuilder {
        UNIXAccountBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct UNIXAccountBuilder {
}

impl UNIXAccountBuilder {
    pub fn build(self) -> UNIXAccount {
        UNIXAccount {
            class_iri: UNIXAccount::CLASS_IRI,
        }
    }
}

impl CaseObject for UNIXAccount {
    fn class_iri() -> &'static str { UNIXAccount::CLASS_IRI }
    fn type_name() -> &'static str { "UNIXAccount" }
}

/// A UNIX account facet is a grouping of characteristics unique to an account on a UNIX operating system.
#[derive(Debug, Clone, Serialize)]
pub struct UNIXAccountFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:gid")]
    pub gid: Option<i64>,
    #[serde(rename = "uco-observable:shell")]
    pub shell: Option<String>,
}

impl UNIXAccountFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXAccountFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> UNIXAccountFacetBuilder {
        UNIXAccountFacetBuilder {
            gid: None,
            shell: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct UNIXAccountFacetBuilder {
    gid: Option<i64>,
    shell: Option<String>,
}

impl UNIXAccountFacetBuilder {
    pub fn gid(mut self, value: i64) -> Self {
        self.gid = Some(value);
        self
    }

    pub fn shell(mut self, value: String) -> Self {
        self.shell = Some(value);
        self
    }

    pub fn build(self) -> UNIXAccountFacet {
        UNIXAccountFacet {
            class_iri: UNIXAccountFacet::CLASS_IRI,
            gid: self.gid,
            shell: self.shell,
        }
    }
}

impl CaseObject for UNIXAccountFacet {
    fn class_iri() -> &'static str { UNIXAccountFacet::CLASS_IRI }
    fn type_name() -> &'static str { "UNIXAccountFacet" }
}

/// A UNIX file is a file pertaining to the UNIX operating system.
#[derive(Debug, Clone, Serialize)]
pub struct UNIXFile {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl UNIXFile {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXFile";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> UNIXFileBuilder {
        UNIXFileBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct UNIXFileBuilder {
}

impl UNIXFileBuilder {
    pub fn build(self) -> UNIXFile {
        UNIXFile {
            class_iri: UNIXFile::CLASS_IRI,
        }
    }
}

impl CaseObject for UNIXFile {
    fn class_iri() -> &'static str { UNIXFile::CLASS_IRI }
    fn type_name() -> &'static str { "UNIXFile" }
}

/// A UNIX file permissions facet is a grouping of characteristics unique to the access rights (e.g., view, change, navigate, execute) of a file on a UNIX file system.
#[derive(Debug, Clone, Serialize)]
pub struct UNIXFilePermissionsFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl UNIXFilePermissionsFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXFilePermissionsFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> UNIXFilePermissionsFacetBuilder {
        UNIXFilePermissionsFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct UNIXFilePermissionsFacetBuilder {
}

impl UNIXFilePermissionsFacetBuilder {
    pub fn build(self) -> UNIXFilePermissionsFacet {
        UNIXFilePermissionsFacet {
            class_iri: UNIXFilePermissionsFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for UNIXFilePermissionsFacet {
    fn class_iri() -> &'static str { UNIXFilePermissionsFacet::CLASS_IRI }
    fn type_name() -> &'static str { "UNIXFilePermissionsFacet" }
}

/// A UNIX process is an instance of a computer program executed on a UNIX operating system.
#[derive(Debug, Clone, Serialize)]
pub struct UNIXProcess {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl UNIXProcess {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXProcess";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> UNIXProcessBuilder {
        UNIXProcessBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct UNIXProcessBuilder {
}

impl UNIXProcessBuilder {
    pub fn build(self) -> UNIXProcess {
        UNIXProcess {
            class_iri: UNIXProcess::CLASS_IRI,
        }
    }
}

impl CaseObject for UNIXProcess {
    fn class_iri() -> &'static str { UNIXProcess::CLASS_IRI }
    fn type_name() -> &'static str { "UNIXProcess" }
}

/// A UNIX process facet is a grouping of characteristics unique to an instance of a computer program executed on a UNIX operating system.
#[derive(Debug, Clone, Serialize)]
pub struct UNIXProcessFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:openFileDescriptor")]
    pub open_file_descriptor: Vec<i64>,
    #[serde(rename = "uco-observable:ruid")]
    pub ruid: Vec<u64>,
}

impl UNIXProcessFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXProcessFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> UNIXProcessFacetBuilder {
        UNIXProcessFacetBuilder {
            open_file_descriptor: Vec::new(),
            ruid: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct UNIXProcessFacetBuilder {
    open_file_descriptor: Vec<i64>,
    ruid: Vec<u64>,
}

impl UNIXProcessFacetBuilder {
    pub fn open_file_descriptor(mut self, value: Vec<i64>) -> Self {
        self.open_file_descriptor = value;
        self
    }

    pub fn ruid(mut self, value: Vec<u64>) -> Self {
        self.ruid = value;
        self
    }

    pub fn build(self) -> UNIXProcessFacet {
        UNIXProcessFacet {
            class_iri: UNIXProcessFacet::CLASS_IRI,
            open_file_descriptor: self.open_file_descriptor,
            ruid: self.ruid,
        }
    }
}

impl CaseObject for UNIXProcessFacet {
    fn class_iri() -> &'static str { UNIXProcessFacet::CLASS_IRI }
    fn type_name() -> &'static str { "UNIXProcessFacet" }
}

/// A UNIX volume facet is a grouping of characteristics unique to a single accessible storage area (volume) with a single UNIX file system. [based on https://en.wikipedia.org/wiki/Volume_(computing)]
#[derive(Debug, Clone, Serialize)]
pub struct UNIXVolumeFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:mountPoint")]
    pub mount_point: Option<String>,
    #[serde(rename = "uco-observable:options")]
    pub options: Option<String>,
}

impl UNIXVolumeFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/UNIXVolumeFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> UNIXVolumeFacetBuilder {
        UNIXVolumeFacetBuilder {
            mount_point: None,
            options: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct UNIXVolumeFacetBuilder {
    mount_point: Option<String>,
    options: Option<String>,
}

impl UNIXVolumeFacetBuilder {
    pub fn mount_point(mut self, value: String) -> Self {
        self.mount_point = Some(value);
        self
    }

    pub fn options(mut self, value: String) -> Self {
        self.options = Some(value);
        self
    }

    pub fn build(self) -> UNIXVolumeFacet {
        UNIXVolumeFacet {
            class_iri: UNIXVolumeFacet::CLASS_IRI,
            mount_point: self.mount_point,
            options: self.options,
        }
    }
}

impl CaseObject for UNIXVolumeFacet {
    fn class_iri() -> &'static str { UNIXVolumeFacet::CLASS_IRI }
    fn type_name() -> &'static str { "UNIXVolumeFacet" }
}

/// A URL is a uniform resource locator (URL) acting as a resolvable address to a particular WWW (World Wide Web) accessible resource.
#[derive(Debug, Clone, Serialize)]
pub struct URL {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl URL {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/URL";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> URLBuilder {
        URLBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct URLBuilder {
}

impl URLBuilder {
    pub fn build(self) -> URL {
        URL {
            class_iri: URL::CLASS_IRI,
        }
    }
}

impl CaseObject for URL {
    fn class_iri() -> &'static str { URL::CLASS_IRI }
    fn type_name() -> &'static str { "URL" }
}

/// A URL facet is a grouping of characteristics unique to a uniform resource locator (URL) acting as a resolvable address to a particular WWW (World Wide Web) accessible resource.
#[derive(Debug, Clone, Serialize)]
pub struct URLFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:fragment")]
    pub fragment: Option<String>,
    #[serde(rename = "uco-observable:fullValue")]
    pub full_value: Option<String>,
    #[serde(rename = "uco-observable:host")]
    pub host: Option<ObservableObject>,
    #[serde(rename = "uco-observable:password")]
    pub password: Option<String>,
    #[serde(rename = "uco-observable:path")]
    pub path: Option<String>,
    #[serde(rename = "uco-observable:port")]
    pub port: Option<i64>,
    #[serde(rename = "uco-observable:query")]
    pub query: Option<String>,
    #[serde(rename = "uco-observable:scheme")]
    pub scheme: Option<String>,
    #[serde(rename = "uco-observable:userName")]
    pub user_name: Option<String>,
}

impl URLFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/URLFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> URLFacetBuilder {
        URLFacetBuilder {
            fragment: None,
            full_value: None,
            host: None,
            password: None,
            path: None,
            port: None,
            query: None,
            scheme: None,
            user_name: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct URLFacetBuilder {
    fragment: Option<String>,
    full_value: Option<String>,
    host: Option<ObservableObject>,
    password: Option<String>,
    path: Option<String>,
    port: Option<i64>,
    query: Option<String>,
    scheme: Option<String>,
    user_name: Option<String>,
}

impl URLFacetBuilder {
    pub fn fragment(mut self, value: String) -> Self {
        self.fragment = Some(value);
        self
    }

    pub fn full_value(mut self, value: String) -> Self {
        self.full_value = Some(value);
        self
    }

    pub fn host(mut self, value: ObservableObject) -> Self {
        self.host = Some(value);
        self
    }

    pub fn password(mut self, value: String) -> Self {
        self.password = Some(value);
        self
    }

    pub fn path(mut self, value: String) -> Self {
        self.path = Some(value);
        self
    }

    pub fn port(mut self, value: i64) -> Self {
        self.port = Some(value);
        self
    }

    pub fn query(mut self, value: String) -> Self {
        self.query = Some(value);
        self
    }

    pub fn scheme(mut self, value: String) -> Self {
        self.scheme = Some(value);
        self
    }

    pub fn user_name(mut self, value: String) -> Self {
        self.user_name = Some(value);
        self
    }

    pub fn build(self) -> URLFacet {
        URLFacet {
            class_iri: URLFacet::CLASS_IRI,
            fragment: self.fragment,
            full_value: self.full_value,
            host: self.host,
            password: self.password,
            path: self.path,
            port: self.port,
            query: self.query,
            scheme: self.scheme,
            user_name: self.user_name,
        }
    }
}

impl CaseObject for URLFacet {
    fn class_iri() -> &'static str { URLFacet::CLASS_IRI }
    fn type_name() -> &'static str { "URLFacet" }
}

/// A URL history characterizes the stored URL history for a particular web browser
#[derive(Debug, Clone, Serialize)]
pub struct URLHistory {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl URLHistory {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/URLHistory";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> URLHistoryBuilder {
        URLHistoryBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct URLHistoryBuilder {
}

impl URLHistoryBuilder {
    pub fn build(self) -> URLHistory {
        URLHistory {
            class_iri: URLHistory::CLASS_IRI,
        }
    }
}

impl CaseObject for URLHistory {
    fn class_iri() -> &'static str { URLHistory::CLASS_IRI }
    fn type_name() -> &'static str { "URLHistory" }
}

/// A URL history entry is a grouping of characteristics unique to the properties of a single URL history entry for a particular browser.
#[derive(Debug, Clone, Serialize)]
pub struct URLHistoryEntry {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:browserUserProfile")]
    pub browser_user_profile: Option<String>,
    #[serde(rename = "uco-observable:expirationTime")]
    pub expiration_time: Option<String>,
    #[serde(rename = "uco-observable:firstVisit")]
    pub first_visit: Option<String>,
    #[serde(rename = "uco-observable:hostname")]
    pub hostname: Option<String>,
    #[serde(rename = "uco-observable:keywordSearchTerm")]
    pub keyword_search_term: Vec<String>,
    #[serde(rename = "uco-observable:lastVisit")]
    pub last_visit: Option<String>,
    #[serde(rename = "uco-observable:manuallyEnteredCount")]
    pub manually_entered_count: Option<u64>,
    #[serde(rename = "uco-observable:pageTitle")]
    pub page_title: Option<String>,
    #[serde(rename = "uco-observable:referrerUrl")]
    pub referrer_url: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:url")]
    pub url: Option<ObservableObject>,
    #[serde(rename = "uco-observable:visitCount")]
    pub visit_count: Option<i64>,
}

impl URLHistoryEntry {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/URLHistoryEntry";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> URLHistoryEntryBuilder {
        URLHistoryEntryBuilder {
            browser_user_profile: None,
            expiration_time: None,
            first_visit: None,
            hostname: None,
            keyword_search_term: Vec::new(),
            last_visit: None,
            manually_entered_count: None,
            page_title: None,
            referrer_url: Vec::new(),
            url: None,
            visit_count: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct URLHistoryEntryBuilder {
    browser_user_profile: Option<String>,
    expiration_time: Option<String>,
    first_visit: Option<String>,
    hostname: Option<String>,
    keyword_search_term: Vec<String>,
    last_visit: Option<String>,
    manually_entered_count: Option<u64>,
    page_title: Option<String>,
    referrer_url: Vec<ObservableObject>,
    url: Option<ObservableObject>,
    visit_count: Option<i64>,
}

impl URLHistoryEntryBuilder {
    pub fn browser_user_profile(mut self, value: String) -> Self {
        self.browser_user_profile = Some(value);
        self
    }

    pub fn expiration_time(mut self, value: String) -> Self {
        self.expiration_time = Some(value);
        self
    }

    pub fn first_visit(mut self, value: String) -> Self {
        self.first_visit = Some(value);
        self
    }

    pub fn hostname(mut self, value: String) -> Self {
        self.hostname = Some(value);
        self
    }

    pub fn keyword_search_term(mut self, value: Vec<String>) -> Self {
        self.keyword_search_term = value;
        self
    }

    pub fn last_visit(mut self, value: String) -> Self {
        self.last_visit = Some(value);
        self
    }

    pub fn manually_entered_count(mut self, value: u64) -> Self {
        self.manually_entered_count = Some(value);
        self
    }

    pub fn page_title(mut self, value: String) -> Self {
        self.page_title = Some(value);
        self
    }

    pub fn referrer_url(mut self, value: Vec<ObservableObject>) -> Self {
        self.referrer_url = value;
        self
    }

    pub fn url(mut self, value: ObservableObject) -> Self {
        self.url = Some(value);
        self
    }

    pub fn visit_count(mut self, value: i64) -> Self {
        self.visit_count = Some(value);
        self
    }

    pub fn build(self) -> URLHistoryEntry {
        URLHistoryEntry {
            class_iri: URLHistoryEntry::CLASS_IRI,
            browser_user_profile: self.browser_user_profile,
            expiration_time: self.expiration_time,
            first_visit: self.first_visit,
            hostname: self.hostname,
            keyword_search_term: self.keyword_search_term,
            last_visit: self.last_visit,
            manually_entered_count: self.manually_entered_count,
            page_title: self.page_title,
            referrer_url: self.referrer_url,
            url: self.url,
            visit_count: self.visit_count,
        }
    }
}

impl CaseObject for URLHistoryEntry {
    fn class_iri() -> &'static str { URLHistoryEntry::CLASS_IRI }
    fn type_name() -> &'static str { "URLHistoryEntry" }
}

/// A URL history facet is a grouping of characteristics unique to the stored URL history for a particular web browser
#[derive(Debug, Clone, Serialize)]
pub struct URLHistoryFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:browserInformation")]
    pub browser_information: Option<ObservableObject>,
    #[serde(rename = "uco-observable:urlHistoryEntry")]
    pub url_history_entry: Vec<URLHistoryEntry>,
}

impl URLHistoryFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/URLHistoryFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> URLHistoryFacetBuilder {
        URLHistoryFacetBuilder {
            browser_information: None,
            url_history_entry: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct URLHistoryFacetBuilder {
    browser_information: Option<ObservableObject>,
    url_history_entry: Vec<URLHistoryEntry>,
}

impl URLHistoryFacetBuilder {
    pub fn browser_information(mut self, value: ObservableObject) -> Self {
        self.browser_information = Some(value);
        self
    }

    pub fn url_history_entry(mut self, value: Vec<URLHistoryEntry>) -> Self {
        self.url_history_entry = value;
        self
    }

    pub fn build(self) -> URLHistoryFacet {
        URLHistoryFacet {
            class_iri: URLHistoryFacet::CLASS_IRI,
            browser_information: self.browser_information,
            url_history_entry: self.url_history_entry,
        }
    }
}

impl CaseObject for URLHistoryFacet {
    fn class_iri() -> &'static str { URLHistoryFacet::CLASS_IRI }
    fn type_name() -> &'static str { "URLHistoryFacet" }
}

/// A URL visit characterizes the properties of a visit of a URL within a particular browser.
#[derive(Debug, Clone, Serialize)]
pub struct URLVisit {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl URLVisit {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/URLVisit";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> URLVisitBuilder {
        URLVisitBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct URLVisitBuilder {
}

impl URLVisitBuilder {
    pub fn build(self) -> URLVisit {
        URLVisit {
            class_iri: URLVisit::CLASS_IRI,
        }
    }
}

impl CaseObject for URLVisit {
    fn class_iri() -> &'static str { URLVisit::CLASS_IRI }
    fn type_name() -> &'static str { "URLVisit" }
}

/// A URL visit facet is a grouping of characteristics unique to the properties of a visit of a URL within a particular browser.
#[derive(Debug, Clone, Serialize)]
pub struct URLVisitFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:browserInformation")]
    pub browser_information: Option<ObservableObject>,
    #[serde(rename = "uco-observable:fromURLVisit")]
    pub from_url_visit: Option<ObservableObject>,
    #[serde(rename = "uco-observable:url")]
    pub url: Option<ObservableObject>,
    #[serde(rename = "uco-observable:urlTransitionType")]
    pub url_transition_type: Vec<String>,
    #[serde(rename = "uco-observable:visitDuration")]
    pub visit_duration: Option<String>,
    #[serde(rename = "uco-observable:visitTime")]
    pub visit_time: Option<String>,
}

impl URLVisitFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/URLVisitFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> URLVisitFacetBuilder {
        URLVisitFacetBuilder {
            browser_information: None,
            from_url_visit: None,
            url: None,
            url_transition_type: Vec::new(),
            visit_duration: None,
            visit_time: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct URLVisitFacetBuilder {
    browser_information: Option<ObservableObject>,
    from_url_visit: Option<ObservableObject>,
    url: Option<ObservableObject>,
    url_transition_type: Vec<String>,
    visit_duration: Option<String>,
    visit_time: Option<String>,
}

impl URLVisitFacetBuilder {
    pub fn browser_information(mut self, value: ObservableObject) -> Self {
        self.browser_information = Some(value);
        self
    }

    pub fn from_url_visit(mut self, value: ObservableObject) -> Self {
        self.from_url_visit = Some(value);
        self
    }

    pub fn url(mut self, value: ObservableObject) -> Self {
        self.url = Some(value);
        self
    }

    pub fn url_transition_type(mut self, value: Vec<String>) -> Self {
        self.url_transition_type = value;
        self
    }

    pub fn visit_duration(mut self, value: String) -> Self {
        self.visit_duration = Some(value);
        self
    }

    pub fn visit_time(mut self, value: String) -> Self {
        self.visit_time = Some(value);
        self
    }

    pub fn build(self) -> URLVisitFacet {
        URLVisitFacet {
            class_iri: URLVisitFacet::CLASS_IRI,
            browser_information: self.browser_information,
            from_url_visit: self.from_url_visit,
            url: self.url,
            url_transition_type: self.url_transition_type,
            visit_duration: self.visit_duration,
            visit_time: self.visit_time,
        }
    }
}

impl CaseObject for URLVisitFacet {
    fn class_iri() -> &'static str { URLVisitFacet::CLASS_IRI }
    fn type_name() -> &'static str { "URLVisitFacet" }
}

/// A user account is an account controlling a user's access to a network, system or platform.
#[derive(Debug, Clone, Serialize)]
pub struct UserAccount {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl UserAccount {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/UserAccount";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> UserAccountBuilder {
        UserAccountBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct UserAccountBuilder {
}

impl UserAccountBuilder {
    pub fn build(self) -> UserAccount {
        UserAccount {
            class_iri: UserAccount::CLASS_IRI,
        }
    }
}

impl CaseObject for UserAccount {
    fn class_iri() -> &'static str { UserAccount::CLASS_IRI }
    fn type_name() -> &'static str { "UserAccount" }
}

/// A user account facet is a grouping of characteristics unique to an account controlling a user's access to a network, system, or platform.
#[derive(Debug, Clone, Serialize)]
pub struct UserAccountFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:canEscalatePrivs")]
    pub can_escalate_privs: Option<bool>,
    #[serde(rename = "uco-observable:homeDirectory")]
    pub home_directory: Option<String>,
    #[serde(rename = "uco-observable:isPrivileged")]
    pub is_privileged: Option<bool>,
    #[serde(rename = "uco-observable:isServiceAccount")]
    pub is_service_account: Option<bool>,
}

impl UserAccountFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/UserAccountFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> UserAccountFacetBuilder {
        UserAccountFacetBuilder {
            can_escalate_privs: None,
            home_directory: None,
            is_privileged: None,
            is_service_account: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct UserAccountFacetBuilder {
    can_escalate_privs: Option<bool>,
    home_directory: Option<String>,
    is_privileged: Option<bool>,
    is_service_account: Option<bool>,
}

impl UserAccountFacetBuilder {
    pub fn can_escalate_privs(mut self, value: bool) -> Self {
        self.can_escalate_privs = Some(value);
        self
    }

    pub fn home_directory(mut self, value: String) -> Self {
        self.home_directory = Some(value);
        self
    }

    pub fn is_privileged(mut self, value: bool) -> Self {
        self.is_privileged = Some(value);
        self
    }

    pub fn is_service_account(mut self, value: bool) -> Self {
        self.is_service_account = Some(value);
        self
    }

    pub fn build(self) -> UserAccountFacet {
        UserAccountFacet {
            class_iri: UserAccountFacet::CLASS_IRI,
            can_escalate_privs: self.can_escalate_privs,
            home_directory: self.home_directory,
            is_privileged: self.is_privileged,
            is_service_account: self.is_service_account,
        }
    }
}

impl CaseObject for UserAccountFacet {
    fn class_iri() -> &'static str { UserAccountFacet::CLASS_IRI }
    fn type_name() -> &'static str { "UserAccountFacet" }
}

/// A user session is a temporary and interactive information interchange between two or more communicating devices within the managed scope of a single user. [based on https://en.wikipedia.org/wiki/Sessi
#[derive(Debug, Clone, Serialize)]
pub struct UserSession {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl UserSession {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/UserSession";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> UserSessionBuilder {
        UserSessionBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct UserSessionBuilder {
}

impl UserSessionBuilder {
    pub fn build(self) -> UserSession {
        UserSession {
            class_iri: UserSession::CLASS_IRI,
        }
    }
}

impl CaseObject for UserSession {
    fn class_iri() -> &'static str { UserSession::CLASS_IRI }
    fn type_name() -> &'static str { "UserSession" }
}

/// A user session facet is a grouping of characteristics unique to a temporary and interactive information interchange between two or more communicating devices within the managed scope of a single user.
#[derive(Debug, Clone, Serialize)]
pub struct UserSessionFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:effectiveGroup")]
    pub effective_group: Option<String>,
    #[serde(rename = "uco-observable:effectiveGroupID")]
    pub effective_group_id: Option<String>,
    #[serde(rename = "uco-observable:effectiveUser")]
    pub effective_user: Option<ObservableObject>,
    #[serde(rename = "uco-observable:loginTime")]
    pub login_time: Option<String>,
    #[serde(rename = "uco-observable:logoutTime")]
    pub logout_time: Option<String>,
}

impl UserSessionFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/UserSessionFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> UserSessionFacetBuilder {
        UserSessionFacetBuilder {
            effective_group: None,
            effective_group_id: None,
            effective_user: None,
            login_time: None,
            logout_time: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct UserSessionFacetBuilder {
    effective_group: Option<String>,
    effective_group_id: Option<String>,
    effective_user: Option<ObservableObject>,
    login_time: Option<String>,
    logout_time: Option<String>,
}

impl UserSessionFacetBuilder {
    pub fn effective_group(mut self, value: String) -> Self {
        self.effective_group = Some(value);
        self
    }

    pub fn effective_group_id(mut self, value: String) -> Self {
        self.effective_group_id = Some(value);
        self
    }

    pub fn effective_user(mut self, value: ObservableObject) -> Self {
        self.effective_user = Some(value);
        self
    }

    pub fn login_time(mut self, value: String) -> Self {
        self.login_time = Some(value);
        self
    }

    pub fn logout_time(mut self, value: String) -> Self {
        self.logout_time = Some(value);
        self
    }

    pub fn build(self) -> UserSessionFacet {
        UserSessionFacet {
            class_iri: UserSessionFacet::CLASS_IRI,
            effective_group: self.effective_group,
            effective_group_id: self.effective_group_id,
            effective_user: self.effective_user,
            login_time: self.login_time,
            logout_time: self.logout_time,
        }
    }
}

impl CaseObject for UserSessionFacet {
    fn class_iri() -> &'static str { UserSessionFacet::CLASS_IRI }
    fn type_name() -> &'static str { "UserSessionFacet" }
}

/// A values enumerated effect facet is a grouping of characteristics unique to the effects of actions upon observable objects where a value of the observable object is enumerated. An example of this woul
#[derive(Debug, Clone, Serialize)]
pub struct ValuesEnumeratedEffectFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:values")]
    pub values: Option<String>,
}

impl ValuesEnumeratedEffectFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/ValuesEnumeratedEffectFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> ValuesEnumeratedEffectFacetBuilder {
        ValuesEnumeratedEffectFacetBuilder {
            values: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct ValuesEnumeratedEffectFacetBuilder {
    values: Option<String>,
}

impl ValuesEnumeratedEffectFacetBuilder {
    pub fn values(mut self, value: String) -> Self {
        self.values = Some(value);
        self
    }

    pub fn build(self) -> ValuesEnumeratedEffectFacet {
        ValuesEnumeratedEffectFacet {
            class_iri: ValuesEnumeratedEffectFacet::CLASS_IRI,
            values: self.values,
        }
    }
}

impl CaseObject for ValuesEnumeratedEffectFacet {
    fn class_iri() -> &'static str { ValuesEnumeratedEffectFacet::CLASS_IRI }
    fn type_name() -> &'static str { "ValuesEnumeratedEffectFacet" }
}

/// A volume is a single accessible storage area (volume) with a single file system. [based on https://en.wikipedia.org/wiki/Volume_(computing)]
#[derive(Debug, Clone, Serialize)]
pub struct Volume {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Volume {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Volume";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> VolumeBuilder {
        VolumeBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct VolumeBuilder {
}

impl VolumeBuilder {
    pub fn build(self) -> Volume {
        Volume {
            class_iri: Volume::CLASS_IRI,
        }
    }
}

impl CaseObject for Volume {
    fn class_iri() -> &'static str { Volume::CLASS_IRI }
    fn type_name() -> &'static str { "Volume" }
}

/// A volume facet is a grouping of characteristics unique to a single accessible storage area (volume) with a single file system. [based on https://en.wikipedia.org/wiki/Volume_(computing)]
#[derive(Debug, Clone, Serialize)]
pub struct VolumeFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:sectorSize")]
    pub sector_size: Option<i64>,
    #[serde(rename = "uco-observable:volumeID")]
    pub volume_id: Option<String>,
}

impl VolumeFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/VolumeFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> VolumeFacetBuilder {
        VolumeFacetBuilder {
            sector_size: None,
            volume_id: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct VolumeFacetBuilder {
    sector_size: Option<i64>,
    volume_id: Option<String>,
}

impl VolumeFacetBuilder {
    pub fn sector_size(mut self, value: i64) -> Self {
        self.sector_size = Some(value);
        self
    }

    pub fn volume_id(mut self, value: String) -> Self {
        self.volume_id = Some(value);
        self
    }

    pub fn build(self) -> VolumeFacet {
        VolumeFacet {
            class_iri: VolumeFacet::CLASS_IRI,
            sector_size: self.sector_size,
            volume_id: self.volume_id,
        }
    }
}

impl CaseObject for VolumeFacet {
    fn class_iri() -> &'static str { VolumeFacet::CLASS_IRI }
    fn type_name() -> &'static str { "VolumeFacet" }
}

/// A wearable device is an electronic device that is designed to be worn on a person's body.
#[derive(Debug, Clone, Serialize)]
pub struct WearableDevice {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WearableDevice {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WearableDevice";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WearableDeviceBuilder {
        WearableDeviceBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WearableDeviceBuilder {
}

impl WearableDeviceBuilder {
    pub fn build(self) -> WearableDevice {
        WearableDevice {
            class_iri: WearableDevice::CLASS_IRI,
        }
    }
}

impl CaseObject for WearableDevice {
    fn class_iri() -> &'static str { WearableDevice::CLASS_IRI }
    fn type_name() -> &'static str { "WearableDevice" }
}

/// A web page is a specific collection of information provided by a website and displayed to a user in a web browser. A website typically consists of many web pages linked together in a coherent fashion.
#[derive(Debug, Clone, Serialize)]
pub struct WebPage {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WebPage {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WebPage";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WebPageBuilder {
        WebPageBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WebPageBuilder {
}

impl WebPageBuilder {
    pub fn build(self) -> WebPage {
        WebPage {
            class_iri: WebPage::CLASS_IRI,
        }
    }
}

impl CaseObject for WebPage {
    fn class_iri() -> &'static str { WebPage::CLASS_IRI }
    fn type_name() -> &'static str { "WebPage" }
}

/// WhoIs is a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https://en.wikipedia.org/wiki/WHOIS]
#[derive(Debug, Clone, Serialize)]
pub struct WhoIs {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WhoIs {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WhoIs";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WhoIsBuilder {
        WhoIsBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WhoIsBuilder {
}

impl WhoIsBuilder {
    pub fn build(self) -> WhoIs {
        WhoIs {
            class_iri: WhoIs::CLASS_IRI,
        }
    }
}

impl CaseObject for WhoIs {
    fn class_iri() -> &'static str { WhoIs::CLASS_IRI }
    fn type_name() -> &'static str { "WhoIs" }
}

/// A whois facet is a grouping of characteristics unique to a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https://en.wikipedia.org/wiki/WHOIS]
#[derive(Debug, Clone, Serialize)]
pub struct WhoIsFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:creationDate")]
    pub creation_date: Option<String>,
    #[serde(rename = "uco-observable:dnssec")]
    pub dnssec: Option<WhoisDNSSECTypeVocab>,
    #[serde(rename = "uco-observable:domainID")]
    pub domain_id: Option<String>,
    #[serde(rename = "uco-observable:domainName")]
    pub domain_name: Option<ObservableObject>,
    #[serde(rename = "uco-observable:expirationDate")]
    pub expiration_date: Option<String>,
    #[serde(rename = "uco-observable:ipAddress")]
    pub ip_address: Option<ObservableObject>,
    #[serde(rename = "uco-observable:lookupDate")]
    pub lookup_date: Option<String>,
    #[serde(rename = "uco-observable:nameServer")]
    pub name_server: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:regionalInternetRegistry")]
    pub regional_internet_registry: Vec<String>,
    #[serde(rename = "uco-observable:registrantContactInfo")]
    pub registrant_contact_info: Option<ObservableObject>,
    #[serde(rename = "uco-observable:registrantIDs")]
    pub registrant_i_ds: Vec<String>,
    #[serde(rename = "uco-observable:registrarInfo")]
    pub registrar_info: Option<WhoisRegistrarInfoType>,
    #[serde(rename = "uco-observable:remarks")]
    pub remarks: Option<String>,
    #[serde(rename = "uco-observable:serverName")]
    pub server_name: Option<ObservableObject>,
    #[serde(rename = "uco-observable:sponsoringRegistrar")]
    pub sponsoring_registrar: Option<String>,
    #[serde(rename = "uco-observable:status")]
    pub status: Vec<String>,
    #[serde(rename = "uco-observable:updatedDate")]
    pub updated_date: Option<String>,
}

impl WhoIsFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WhoIsFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WhoIsFacetBuilder {
        WhoIsFacetBuilder {
            creation_date: None,
            dnssec: None,
            domain_id: None,
            domain_name: None,
            expiration_date: None,
            ip_address: None,
            lookup_date: None,
            name_server: Vec::new(),
            regional_internet_registry: Vec::new(),
            registrant_contact_info: None,
            registrant_i_ds: Vec::new(),
            registrar_info: None,
            remarks: None,
            server_name: None,
            sponsoring_registrar: None,
            status: Vec::new(),
            updated_date: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WhoIsFacetBuilder {
    creation_date: Option<String>,
    dnssec: Option<WhoisDNSSECTypeVocab>,
    domain_id: Option<String>,
    domain_name: Option<ObservableObject>,
    expiration_date: Option<String>,
    ip_address: Option<ObservableObject>,
    lookup_date: Option<String>,
    name_server: Vec<ObservableObject>,
    regional_internet_registry: Vec<String>,
    registrant_contact_info: Option<ObservableObject>,
    registrant_i_ds: Vec<String>,
    registrar_info: Option<WhoisRegistrarInfoType>,
    remarks: Option<String>,
    server_name: Option<ObservableObject>,
    sponsoring_registrar: Option<String>,
    status: Vec<String>,
    updated_date: Option<String>,
}

impl WhoIsFacetBuilder {
    pub fn creation_date(mut self, value: String) -> Self {
        self.creation_date = Some(value);
        self
    }

    pub fn dnssec(mut self, value: WhoisDNSSECTypeVocab) -> Self {
        self.dnssec = Some(value);
        self
    }

    pub fn domain_id(mut self, value: String) -> Self {
        self.domain_id = Some(value);
        self
    }

    pub fn domain_name(mut self, value: ObservableObject) -> Self {
        self.domain_name = Some(value);
        self
    }

    pub fn expiration_date(mut self, value: String) -> Self {
        self.expiration_date = Some(value);
        self
    }

    pub fn ip_address(mut self, value: ObservableObject) -> Self {
        self.ip_address = Some(value);
        self
    }

    pub fn lookup_date(mut self, value: String) -> Self {
        self.lookup_date = Some(value);
        self
    }

    pub fn name_server(mut self, value: Vec<ObservableObject>) -> Self {
        self.name_server = value;
        self
    }

    pub fn regional_internet_registry(mut self, value: Vec<String>) -> Self {
        self.regional_internet_registry = value;
        self
    }

    pub fn registrant_contact_info(mut self, value: ObservableObject) -> Self {
        self.registrant_contact_info = Some(value);
        self
    }

    pub fn registrant_i_ds(mut self, value: Vec<String>) -> Self {
        self.registrant_i_ds = value;
        self
    }

    pub fn registrar_info(mut self, value: WhoisRegistrarInfoType) -> Self {
        self.registrar_info = Some(value);
        self
    }

    pub fn remarks(mut self, value: String) -> Self {
        self.remarks = Some(value);
        self
    }

    pub fn server_name(mut self, value: ObservableObject) -> Self {
        self.server_name = Some(value);
        self
    }

    pub fn sponsoring_registrar(mut self, value: String) -> Self {
        self.sponsoring_registrar = Some(value);
        self
    }

    pub fn status(mut self, value: Vec<String>) -> Self {
        self.status = value;
        self
    }

    pub fn updated_date(mut self, value: String) -> Self {
        self.updated_date = Some(value);
        self
    }

    pub fn build(self) -> WhoIsFacet {
        WhoIsFacet {
            class_iri: WhoIsFacet::CLASS_IRI,
            creation_date: self.creation_date,
            dnssec: self.dnssec,
            domain_id: self.domain_id,
            domain_name: self.domain_name,
            expiration_date: self.expiration_date,
            ip_address: self.ip_address,
            lookup_date: self.lookup_date,
            name_server: self.name_server,
            regional_internet_registry: self.regional_internet_registry,
            registrant_contact_info: self.registrant_contact_info,
            registrant_i_ds: self.registrant_i_ds,
            registrar_info: self.registrar_info,
            remarks: self.remarks,
            server_name: self.server_name,
            sponsoring_registrar: self.sponsoring_registrar,
            status: self.status,
            updated_date: self.updated_date,
        }
    }
}

impl CaseObject for WhoIsFacet {
    fn class_iri() -> &'static str { WhoIsFacet::CLASS_IRI }
    fn type_name() -> &'static str { "WhoIsFacet" }
}

/// A Whois contact type is a grouping of characteristics unique to contact-related information present in a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https://en.wiki
#[derive(Debug, Clone, Serialize)]
pub struct WhoisContactFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:whoisContactType")]
    pub whois_contact_type: Vec<String>,
}

impl WhoisContactFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WhoisContactFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WhoisContactFacetBuilder {
        WhoisContactFacetBuilder {
            whois_contact_type: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WhoisContactFacetBuilder {
    whois_contact_type: Vec<String>,
}

impl WhoisContactFacetBuilder {
    pub fn whois_contact_type(mut self, value: Vec<String>) -> Self {
        self.whois_contact_type = value;
        self
    }

    pub fn build(self) -> WhoisContactFacet {
        WhoisContactFacet {
            class_iri: WhoisContactFacet::CLASS_IRI,
            whois_contact_type: self.whois_contact_type,
        }
    }
}

impl CaseObject for WhoisContactFacet {
    fn class_iri() -> &'static str { WhoisContactFacet::CLASS_IRI }
    fn type_name() -> &'static str { "WhoisContactFacet" }
}

/// A Whois registrar info type is a grouping of characteristics unique to registrar-related information present in a response record conformant to the WHOIS protocol standard (RFC 3912). [based on https:
#[derive(Debug, Clone, Serialize)]
pub struct WhoisRegistrarInfoType {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:contactPhoneNumber")]
    pub contact_phone_number: Option<ObservableObject>,
    #[serde(rename = "uco-observable:emailAddress")]
    pub email_address: Option<ObservableObject>,
    #[serde(rename = "uco-observable:geolocationAddress")]
    pub geolocation_address: Option<Location>,
    #[serde(rename = "uco-observable:referralURL")]
    pub referral_url: Option<ObservableObject>,
    #[serde(rename = "uco-observable:registrarGUID")]
    pub registrar_guid: Option<String>,
    #[serde(rename = "uco-observable:registrarID")]
    pub registrar_id: Option<String>,
    #[serde(rename = "uco-observable:registrarName")]
    pub registrar_name: Option<String>,
    #[serde(rename = "uco-observable:whoisServer")]
    pub whois_server: Option<ObservableObject>,
}

impl WhoisRegistrarInfoType {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WhoisRegistrarInfoType";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WhoisRegistrarInfoTypeBuilder {
        WhoisRegistrarInfoTypeBuilder {
            contact_phone_number: None,
            email_address: None,
            geolocation_address: None,
            referral_url: None,
            registrar_guid: None,
            registrar_id: None,
            registrar_name: None,
            whois_server: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WhoisRegistrarInfoTypeBuilder {
    contact_phone_number: Option<ObservableObject>,
    email_address: Option<ObservableObject>,
    geolocation_address: Option<Location>,
    referral_url: Option<ObservableObject>,
    registrar_guid: Option<String>,
    registrar_id: Option<String>,
    registrar_name: Option<String>,
    whois_server: Option<ObservableObject>,
}

impl WhoisRegistrarInfoTypeBuilder {
    pub fn contact_phone_number(mut self, value: ObservableObject) -> Self {
        self.contact_phone_number = Some(value);
        self
    }

    pub fn email_address(mut self, value: ObservableObject) -> Self {
        self.email_address = Some(value);
        self
    }

    pub fn geolocation_address(mut self, value: Location) -> Self {
        self.geolocation_address = Some(value);
        self
    }

    pub fn referral_url(mut self, value: ObservableObject) -> Self {
        self.referral_url = Some(value);
        self
    }

    pub fn registrar_guid(mut self, value: String) -> Self {
        self.registrar_guid = Some(value);
        self
    }

    pub fn registrar_id(mut self, value: String) -> Self {
        self.registrar_id = Some(value);
        self
    }

    pub fn registrar_name(mut self, value: String) -> Self {
        self.registrar_name = Some(value);
        self
    }

    pub fn whois_server(mut self, value: ObservableObject) -> Self {
        self.whois_server = Some(value);
        self
    }

    pub fn build(self) -> WhoisRegistrarInfoType {
        WhoisRegistrarInfoType {
            class_iri: WhoisRegistrarInfoType::CLASS_IRI,
            contact_phone_number: self.contact_phone_number,
            email_address: self.email_address,
            geolocation_address: self.geolocation_address,
            referral_url: self.referral_url,
            registrar_guid: self.registrar_guid,
            registrar_id: self.registrar_id,
            registrar_name: self.registrar_name,
            whois_server: self.whois_server,
        }
    }
}

impl CaseObject for WhoisRegistrarInfoType {
    fn class_iri() -> &'static str { WhoisRegistrarInfoType::CLASS_IRI }
    fn type_name() -> &'static str { "WhoisRegistrarInfoType" }
}

/// A Wi-Fi address is a media access control (MAC) standards-conformant identifier assigned to a device network interface to enable routing and management of IEEE 802.11 standards-conformant communicatio
#[derive(Debug, Clone, Serialize)]
pub struct WifiAddress {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WifiAddress {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WifiAddress";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WifiAddressBuilder {
        WifiAddressBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WifiAddressBuilder {
}

impl WifiAddressBuilder {
    pub fn build(self) -> WifiAddress {
        WifiAddress {
            class_iri: WifiAddress::CLASS_IRI,
        }
    }
}

impl CaseObject for WifiAddress {
    fn class_iri() -> &'static str { WifiAddress::CLASS_IRI }
    fn type_name() -> &'static str { "WifiAddress" }
}

/// A Wi-Fi address facet is a grouping of characteristics unique to a media access control (MAC) standards conformant identifier assigned to a device network interface to enable routing and management of
#[derive(Debug, Clone, Serialize)]
pub struct WifiAddressFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WifiAddressFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WifiAddressFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WifiAddressFacetBuilder {
        WifiAddressFacetBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WifiAddressFacetBuilder {
}

impl WifiAddressFacetBuilder {
    pub fn build(self) -> WifiAddressFacet {
        WifiAddressFacet {
            class_iri: WifiAddressFacet::CLASS_IRI,
        }
    }
}

impl CaseObject for WifiAddressFacet {
    fn class_iri() -> &'static str { WifiAddressFacet::CLASS_IRI }
    fn type_name() -> &'static str { "WifiAddressFacet" }
}

/// A wiki is an online hypertext publication collaboratively edited and managed by its own audience directly using a web browser. A typical wiki contains multiple pages/articles for the subjects or scope
#[derive(Debug, Clone, Serialize)]
pub struct Wiki {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl Wiki {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/Wiki";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WikiBuilder {
        WikiBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WikiBuilder {
}

impl WikiBuilder {
    pub fn build(self) -> Wiki {
        Wiki {
            class_iri: Wiki::CLASS_IRI,
        }
    }
}

impl CaseObject for Wiki {
    fn class_iri() -> &'static str { Wiki::CLASS_IRI }
    fn type_name() -> &'static str { "Wiki" }
}

/// A wiki article is one or more pages in a wiki focused on characterizing a particular topic.
#[derive(Debug, Clone, Serialize)]
pub struct WikiArticle {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WikiArticle {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WikiArticle";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WikiArticleBuilder {
        WikiArticleBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WikiArticleBuilder {
}

impl WikiArticleBuilder {
    pub fn build(self) -> WikiArticle {
        WikiArticle {
            class_iri: WikiArticle::CLASS_IRI,
        }
    }
}

impl CaseObject for WikiArticle {
    fn class_iri() -> &'static str { WikiArticle::CLASS_IRI }
    fn type_name() -> &'static str { "WikiArticle" }
}

/// A Windows account is a user account on a Windows operating system.
#[derive(Debug, Clone, Serialize)]
pub struct WindowsAccount {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsAccount {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsAccount";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsAccountBuilder {
        WindowsAccountBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsAccountBuilder {
}

impl WindowsAccountBuilder {
    pub fn build(self) -> WindowsAccount {
        WindowsAccount {
            class_iri: WindowsAccount::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsAccount {
    fn class_iri() -> &'static str { WindowsAccount::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsAccount" }
}

/// A Windows account facet is a grouping of characteristics unique to a user account on a Windows operating system.
#[derive(Debug, Clone, Serialize)]
pub struct WindowsAccountFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:groups")]
    pub groups: Vec<String>,
}

impl WindowsAccountFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsAccountFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsAccountFacetBuilder {
        WindowsAccountFacetBuilder {
            groups: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsAccountFacetBuilder {
    groups: Vec<String>,
}

impl WindowsAccountFacetBuilder {
    pub fn groups(mut self, value: Vec<String>) -> Self {
        self.groups = value;
        self
    }

    pub fn build(self) -> WindowsAccountFacet {
        WindowsAccountFacet {
            class_iri: WindowsAccountFacet::CLASS_IRI,
            groups: self.groups,
        }
    }
}

impl CaseObject for WindowsAccountFacet {
    fn class_iri() -> &'static str { WindowsAccountFacet::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsAccountFacet" }
}

/// A Windows Active Directory account is an account managed by directory-based identity-related services of a Windows operating system.
#[derive(Debug, Clone, Serialize)]
pub struct WindowsActiveDirectoryAccount {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsActiveDirectoryAccount {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsActiveDirectoryAccount";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsActiveDirectoryAccountBuilder {
        WindowsActiveDirectoryAccountBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsActiveDirectoryAccountBuilder {
}

impl WindowsActiveDirectoryAccountBuilder {
    pub fn build(self) -> WindowsActiveDirectoryAccount {
        WindowsActiveDirectoryAccount {
            class_iri: WindowsActiveDirectoryAccount::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsActiveDirectoryAccount {
    fn class_iri() -> &'static str { WindowsActiveDirectoryAccount::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsActiveDirectoryAccount" }
}

/// A Windows Active Directory account facet is a grouping of characteristics unique to an account managed by directory-based identity-related services of a Windows operating system.
#[derive(Debug, Clone, Serialize)]
pub struct WindowsActiveDirectoryAccountFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:activeDirectoryGroups")]
    pub active_directory_groups: Vec<String>,
    #[serde(rename = "uco-observable:objectGUID")]
    pub object_guid: Option<String>,
}

impl WindowsActiveDirectoryAccountFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsActiveDirectoryAccountFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsActiveDirectoryAccountFacetBuilder {
        WindowsActiveDirectoryAccountFacetBuilder {
            active_directory_groups: Vec::new(),
            object_guid: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsActiveDirectoryAccountFacetBuilder {
    active_directory_groups: Vec<String>,
    object_guid: Option<String>,
}

impl WindowsActiveDirectoryAccountFacetBuilder {
    pub fn active_directory_groups(mut self, value: Vec<String>) -> Self {
        self.active_directory_groups = value;
        self
    }

    pub fn object_guid(mut self, value: String) -> Self {
        self.object_guid = Some(value);
        self
    }

    pub fn build(self) -> WindowsActiveDirectoryAccountFacet {
        WindowsActiveDirectoryAccountFacet {
            class_iri: WindowsActiveDirectoryAccountFacet::CLASS_IRI,
            active_directory_groups: self.active_directory_groups,
            object_guid: self.object_guid,
        }
    }
}

impl CaseObject for WindowsActiveDirectoryAccountFacet {
    fn class_iri() -> &'static str { WindowsActiveDirectoryAccountFacet::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsActiveDirectoryAccountFacet" }
}

/// A Windows computer specification is the hardware ans software of a programmable electronic device that can store, retrieve, and process data running a Microsoft Windows operating system. [based on mer
#[derive(Debug, Clone, Serialize)]
pub struct WindowsComputerSpecification {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsComputerSpecification {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsComputerSpecification";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsComputerSpecificationBuilder {
        WindowsComputerSpecificationBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsComputerSpecificationBuilder {
}

impl WindowsComputerSpecificationBuilder {
    pub fn build(self) -> WindowsComputerSpecification {
        WindowsComputerSpecification {
            class_iri: WindowsComputerSpecification::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsComputerSpecification {
    fn class_iri() -> &'static str { WindowsComputerSpecification::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsComputerSpecification" }
}

/// A Windows computer specification facet is a grouping of characteristics unique to the hardware and software of a programmable electronic device that can store, retrieve, and process data running a Mic
#[derive(Debug, Clone, Serialize)]
pub struct WindowsComputerSpecificationFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:domain")]
    pub domain: Vec<String>,
    #[serde(rename = "uco-observable:globalFlagList")]
    pub global_flag_list: Vec<GlobalFlagType>,
    #[serde(rename = "uco-observable:lastShutdownDate")]
    pub last_shutdown_date: Option<String>,
    #[serde(rename = "uco-observable:msProductID")]
    pub ms_product_id: Option<String>,
    #[serde(rename = "uco-observable:msProductName")]
    pub ms_product_name: Option<String>,
    #[serde(rename = "uco-observable:netBIOSName")]
    pub net_bios_name: Option<String>,
    #[serde(rename = "uco-observable:osInstallDate")]
    pub os_install_date: Option<String>,
    #[serde(rename = "uco-observable:osLastUpgradeDate")]
    pub os_last_upgrade_date: Option<String>,
    #[serde(rename = "uco-observable:registeredOrganization")]
    pub registered_organization: Option<Identity>,
    #[serde(rename = "uco-observable:registeredOwner")]
    pub registered_owner: Option<Identity>,
    #[serde(rename = "uco-observable:windowsDirectory")]
    pub windows_directory: Option<ObservableObject>,
    #[serde(rename = "uco-observable:windowsSystemDirectory")]
    pub windows_system_directory: Option<ObservableObject>,
    #[serde(rename = "uco-observable:windowsTempDirectory")]
    pub windows_temp_directory: Option<ObservableObject>,
}

impl WindowsComputerSpecificationFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsComputerSpecificationFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsComputerSpecificationFacetBuilder {
        WindowsComputerSpecificationFacetBuilder {
            domain: Vec::new(),
            global_flag_list: Vec::new(),
            last_shutdown_date: None,
            ms_product_id: None,
            ms_product_name: None,
            net_bios_name: None,
            os_install_date: None,
            os_last_upgrade_date: None,
            registered_organization: None,
            registered_owner: None,
            windows_directory: None,
            windows_system_directory: None,
            windows_temp_directory: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsComputerSpecificationFacetBuilder {
    domain: Vec<String>,
    global_flag_list: Vec<GlobalFlagType>,
    last_shutdown_date: Option<String>,
    ms_product_id: Option<String>,
    ms_product_name: Option<String>,
    net_bios_name: Option<String>,
    os_install_date: Option<String>,
    os_last_upgrade_date: Option<String>,
    registered_organization: Option<Identity>,
    registered_owner: Option<Identity>,
    windows_directory: Option<ObservableObject>,
    windows_system_directory: Option<ObservableObject>,
    windows_temp_directory: Option<ObservableObject>,
}

impl WindowsComputerSpecificationFacetBuilder {
    pub fn domain(mut self, value: Vec<String>) -> Self {
        self.domain = value;
        self
    }

    pub fn global_flag_list(mut self, value: Vec<GlobalFlagType>) -> Self {
        self.global_flag_list = value;
        self
    }

    pub fn last_shutdown_date(mut self, value: String) -> Self {
        self.last_shutdown_date = Some(value);
        self
    }

    pub fn ms_product_id(mut self, value: String) -> Self {
        self.ms_product_id = Some(value);
        self
    }

    pub fn ms_product_name(mut self, value: String) -> Self {
        self.ms_product_name = Some(value);
        self
    }

    pub fn net_bios_name(mut self, value: String) -> Self {
        self.net_bios_name = Some(value);
        self
    }

    pub fn os_install_date(mut self, value: String) -> Self {
        self.os_install_date = Some(value);
        self
    }

    pub fn os_last_upgrade_date(mut self, value: String) -> Self {
        self.os_last_upgrade_date = Some(value);
        self
    }

    pub fn registered_organization(mut self, value: Identity) -> Self {
        self.registered_organization = Some(value);
        self
    }

    pub fn registered_owner(mut self, value: Identity) -> Self {
        self.registered_owner = Some(value);
        self
    }

    pub fn windows_directory(mut self, value: ObservableObject) -> Self {
        self.windows_directory = Some(value);
        self
    }

    pub fn windows_system_directory(mut self, value: ObservableObject) -> Self {
        self.windows_system_directory = Some(value);
        self
    }

    pub fn windows_temp_directory(mut self, value: ObservableObject) -> Self {
        self.windows_temp_directory = Some(value);
        self
    }

    pub fn build(self) -> WindowsComputerSpecificationFacet {
        WindowsComputerSpecificationFacet {
            class_iri: WindowsComputerSpecificationFacet::CLASS_IRI,
            domain: self.domain,
            global_flag_list: self.global_flag_list,
            last_shutdown_date: self.last_shutdown_date,
            ms_product_id: self.ms_product_id,
            ms_product_name: self.ms_product_name,
            net_bios_name: self.net_bios_name,
            os_install_date: self.os_install_date,
            os_last_upgrade_date: self.os_last_upgrade_date,
            registered_organization: self.registered_organization,
            registered_owner: self.registered_owner,
            windows_directory: self.windows_directory,
            windows_system_directory: self.windows_system_directory,
            windows_temp_directory: self.windows_temp_directory,
        }
    }
}

impl CaseObject for WindowsComputerSpecificationFacet {
    fn class_iri() -> &'static str { WindowsComputerSpecificationFacet::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsComputerSpecificationFacet" }
}

/// A Windows critical section is a Windows object that provides synchronization similar to that provided by a mutex object, except that a critical section can be used only by the threads of a single proc
#[derive(Debug, Clone, Serialize)]
pub struct WindowsCriticalSection {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsCriticalSection {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsCriticalSection";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsCriticalSectionBuilder {
        WindowsCriticalSectionBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsCriticalSectionBuilder {
}

impl WindowsCriticalSectionBuilder {
    pub fn build(self) -> WindowsCriticalSection {
        WindowsCriticalSection {
            class_iri: WindowsCriticalSection::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsCriticalSection {
    fn class_iri() -> &'static str { WindowsCriticalSection::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsCriticalSection" }
}

/// A Windows event is a notification record of an occurance of interest (system, security, application, etc.) on a Windows operating system.
#[derive(Debug, Clone, Serialize)]
pub struct WindowsEvent {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsEvent {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsEvent";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsEventBuilder {
        WindowsEventBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsEventBuilder {
}

impl WindowsEventBuilder {
    pub fn build(self) -> WindowsEvent {
        WindowsEvent {
            class_iri: WindowsEvent::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsEvent {
    fn class_iri() -> &'static str { WindowsEvent::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsEvent" }
}

/// A Windows file mapping is the association of a file's contents with a portion of the virtual address space of a process within a Windows operating system. The system creates a file mapping object (als
#[derive(Debug, Clone, Serialize)]
pub struct WindowsFilemapping {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsFilemapping {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsFilemapping";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsFilemappingBuilder {
        WindowsFilemappingBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsFilemappingBuilder {
}

impl WindowsFilemappingBuilder {
    pub fn build(self) -> WindowsFilemapping {
        WindowsFilemapping {
            class_iri: WindowsFilemapping::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsFilemapping {
    fn class_iri() -> &'static str { WindowsFilemapping::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsFilemapping" }
}

/// A Windows handle is an abstract reference to a resource within the Windows operating system, such as a window, memory, an open file or a pipe. It is the mechanism by which applications interact with s
#[derive(Debug, Clone, Serialize)]
pub struct WindowsHandle {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsHandle {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsHandle";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsHandleBuilder {
        WindowsHandleBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsHandleBuilder {
}

impl WindowsHandleBuilder {
    pub fn build(self) -> WindowsHandle {
        WindowsHandle {
            class_iri: WindowsHandle::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsHandle {
    fn class_iri() -> &'static str { WindowsHandle::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsHandle" }
}

/// A Windows hook is a mechanism by which an application can intercept events, such as messages, mouse actions, and keystrokes within the Windows operating system. A function that intercepts a particular
#[derive(Debug, Clone, Serialize)]
pub struct WindowsHook {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsHook {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsHook";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsHookBuilder {
        WindowsHookBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsHookBuilder {
}

impl WindowsHookBuilder {
    pub fn build(self) -> WindowsHook {
        WindowsHook {
            class_iri: WindowsHook::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsHook {
    fn class_iri() -> &'static str { WindowsHook::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsHook" }
}

/// A Windows mailslot is is a pseudofile that resides in memory, and may be accessed using standard file functions. The data in a mailslot message can be in any form, but cannot be larger than 424 bytes 
#[derive(Debug, Clone, Serialize)]
pub struct WindowsMailslot {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsMailslot {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsMailslot";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsMailslotBuilder {
        WindowsMailslotBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsMailslotBuilder {
}

impl WindowsMailslotBuilder {
    pub fn build(self) -> WindowsMailslot {
        WindowsMailslot {
            class_iri: WindowsMailslot::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsMailslot {
    fn class_iri() -> &'static str { WindowsMailslot::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsMailslot" }
}

/// A Windows network share is a Windows computer resource made available from one host to other hosts on a computer network. It is a device or piece of information on a computer that can be remotely acce
#[derive(Debug, Clone, Serialize)]
pub struct WindowsNetworkShare {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsNetworkShare {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsNetworkShare";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsNetworkShareBuilder {
        WindowsNetworkShareBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsNetworkShareBuilder {
}

impl WindowsNetworkShareBuilder {
    pub fn build(self) -> WindowsNetworkShare {
        WindowsNetworkShare {
            class_iri: WindowsNetworkShare::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsNetworkShare {
    fn class_iri() -> &'static str { WindowsNetworkShare::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsNetworkShare" }
}

/// A Windows PE binary file is a Windows portable executable (PE) file.
#[derive(Debug, Clone, Serialize)]
pub struct WindowsPEBinaryFile {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsPEBinaryFile {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEBinaryFile";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsPEBinaryFileBuilder {
        WindowsPEBinaryFileBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsPEBinaryFileBuilder {
}

impl WindowsPEBinaryFileBuilder {
    pub fn build(self) -> WindowsPEBinaryFile {
        WindowsPEBinaryFile {
            class_iri: WindowsPEBinaryFile::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsPEBinaryFile {
    fn class_iri() -> &'static str { WindowsPEBinaryFile::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsPEBinaryFile" }
}

/// A Windows PE binary file facet is a grouping of characteristics unique to a Windows portable executable (PE) file.
#[derive(Debug, Clone, Serialize)]
pub struct WindowsPEBinaryFileFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:characteristics")]
    pub characteristics: Vec<u16>,
    #[serde(rename = "uco-observable:fileHeaderHashes")]
    pub file_header_hashes: Vec<Hash>,
    #[serde(rename = "uco-observable:impHash")]
    pub imp_hash: Option<String>,
    #[serde(rename = "uco-observable:machine")]
    pub machine: Vec<String>,
    #[serde(rename = "uco-observable:numberOfSections")]
    pub number_of_sections: Option<i64>,
    #[serde(rename = "uco-observable:numberOfSymbols")]
    pub number_of_symbols: Option<i64>,
    #[serde(rename = "uco-observable:optionalHeader")]
    pub optional_header: Option<WindowsPEOptionalHeader>,
    #[serde(rename = "uco-observable:peType")]
    pub pe_type: Option<String>,
    #[serde(rename = "uco-observable:pointerToSymbolTable")]
    pub pointer_to_symbol_table: Vec<Vec<u8>>,
    #[serde(rename = "uco-observable:sections")]
    pub sections: Vec<WindowsPESection>,
    #[serde(rename = "uco-observable:sizeOfOptionalHeader")]
    pub size_of_optional_header: Option<i64>,
    #[serde(rename = "uco-observable:timeDateStamp")]
    pub time_date_stamp: Option<String>,
}

impl WindowsPEBinaryFileFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEBinaryFileFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsPEBinaryFileFacetBuilder {
        WindowsPEBinaryFileFacetBuilder {
            characteristics: Vec::new(),
            file_header_hashes: Vec::new(),
            imp_hash: None,
            machine: Vec::new(),
            number_of_sections: None,
            number_of_symbols: None,
            optional_header: None,
            pe_type: None,
            pointer_to_symbol_table: Vec::new(),
            sections: Vec::new(),
            size_of_optional_header: None,
            time_date_stamp: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsPEBinaryFileFacetBuilder {
    characteristics: Vec<u16>,
    file_header_hashes: Vec<Hash>,
    imp_hash: Option<String>,
    machine: Vec<String>,
    number_of_sections: Option<i64>,
    number_of_symbols: Option<i64>,
    optional_header: Option<WindowsPEOptionalHeader>,
    pe_type: Option<String>,
    pointer_to_symbol_table: Vec<Vec<u8>>,
    sections: Vec<WindowsPESection>,
    size_of_optional_header: Option<i64>,
    time_date_stamp: Option<String>,
}

impl WindowsPEBinaryFileFacetBuilder {
    pub fn characteristics(mut self, value: Vec<u16>) -> Self {
        self.characteristics = value;
        self
    }

    pub fn file_header_hashes(mut self, value: Vec<Hash>) -> Self {
        self.file_header_hashes = value;
        self
    }

    pub fn imp_hash(mut self, value: String) -> Self {
        self.imp_hash = Some(value);
        self
    }

    pub fn machine(mut self, value: Vec<String>) -> Self {
        self.machine = value;
        self
    }

    pub fn number_of_sections(mut self, value: i64) -> Self {
        self.number_of_sections = Some(value);
        self
    }

    pub fn number_of_symbols(mut self, value: i64) -> Self {
        self.number_of_symbols = Some(value);
        self
    }

    pub fn optional_header(mut self, value: WindowsPEOptionalHeader) -> Self {
        self.optional_header = Some(value);
        self
    }

    pub fn pe_type(mut self, value: String) -> Self {
        self.pe_type = Some(value);
        self
    }

    pub fn pointer_to_symbol_table(mut self, value: Vec<Vec<u8>>) -> Self {
        self.pointer_to_symbol_table = value;
        self
    }

    pub fn sections(mut self, value: Vec<WindowsPESection>) -> Self {
        self.sections = value;
        self
    }

    pub fn size_of_optional_header(mut self, value: i64) -> Self {
        self.size_of_optional_header = Some(value);
        self
    }

    pub fn time_date_stamp(mut self, value: String) -> Self {
        self.time_date_stamp = Some(value);
        self
    }

    pub fn build(self) -> WindowsPEBinaryFileFacet {
        WindowsPEBinaryFileFacet {
            class_iri: WindowsPEBinaryFileFacet::CLASS_IRI,
            characteristics: self.characteristics,
            file_header_hashes: self.file_header_hashes,
            imp_hash: self.imp_hash,
            machine: self.machine,
            number_of_sections: self.number_of_sections,
            number_of_symbols: self.number_of_symbols,
            optional_header: self.optional_header,
            pe_type: self.pe_type,
            pointer_to_symbol_table: self.pointer_to_symbol_table,
            sections: self.sections,
            size_of_optional_header: self.size_of_optional_header,
            time_date_stamp: self.time_date_stamp,
        }
    }
}

impl CaseObject for WindowsPEBinaryFileFacet {
    fn class_iri() -> &'static str { WindowsPEBinaryFileFacet::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsPEBinaryFileFacet" }
}

/// A Windows PE file header is a grouping of characteristics unique to the 'header' of a Windows PE (Portable Executable) file, consisting of a collection of metadata about the overall nature and structu
#[derive(Debug, Clone, Serialize)]
pub struct WindowsPEFileHeader {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:timeDateStamp")]
    pub time_date_stamp: Option<String>,
}

impl WindowsPEFileHeader {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEFileHeader";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsPEFileHeaderBuilder {
        WindowsPEFileHeaderBuilder {
            time_date_stamp: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsPEFileHeaderBuilder {
    time_date_stamp: Option<String>,
}

impl WindowsPEFileHeaderBuilder {
    pub fn time_date_stamp(mut self, value: String) -> Self {
        self.time_date_stamp = Some(value);
        self
    }

    pub fn build(self) -> WindowsPEFileHeader {
        WindowsPEFileHeader {
            class_iri: WindowsPEFileHeader::CLASS_IRI,
            time_date_stamp: self.time_date_stamp,
        }
    }
}

impl CaseObject for WindowsPEFileHeader {
    fn class_iri() -> &'static str { WindowsPEFileHeader::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsPEFileHeader" }
}

/// A Windows PE optional header is a grouping of characteristics unique to the 'optional header' of a Windows PE (Portable Executable) file, consisting of a collection of metadata about the executable co
#[derive(Debug, Clone, Serialize)]
pub struct WindowsPEOptionalHeader {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:addressOfEntryPoint")]
    pub address_of_entry_point: Vec<u32>,
    #[serde(rename = "uco-observable:baseOfCode")]
    pub base_of_code: Vec<u32>,
    #[serde(rename = "uco-observable:checksum")]
    pub checksum: Vec<u32>,
    #[serde(rename = "uco-observable:dllCharacteristics")]
    pub dll_characteristics: Vec<u16>,
    #[serde(rename = "uco-observable:fileAlignment")]
    pub file_alignment: Vec<u32>,
    #[serde(rename = "uco-observable:imageBase")]
    pub image_base: Vec<u32>,
    #[serde(rename = "uco-observable:loaderFlags")]
    pub loader_flags: Vec<u32>,
    #[serde(rename = "uco-observable:magic")]
    pub magic: Vec<u16>,
    #[serde(rename = "uco-observable:majorImageVersion")]
    pub major_image_version: Vec<u16>,
    #[serde(rename = "uco-observable:majorLinkerVersion")]
    pub major_linker_version: Vec<i8>,
    #[serde(rename = "uco-observable:majorOSVersion")]
    pub major_os_version: Vec<u16>,
    #[serde(rename = "uco-observable:majorSubsystemVersion")]
    pub major_subsystem_version: Vec<u16>,
    #[serde(rename = "uco-observable:minorImageVersion")]
    pub minor_image_version: Vec<u16>,
    #[serde(rename = "uco-observable:minorLinkerVersion")]
    pub minor_linker_version: Vec<i8>,
    #[serde(rename = "uco-observable:minorOSVersion")]
    pub minor_os_version: Vec<u16>,
    #[serde(rename = "uco-observable:minorSubsystemVersion")]
    pub minor_subsystem_version: Vec<u16>,
    #[serde(rename = "uco-observable:numberOfRVAAndSizes")]
    pub number_of_rva_and_sizes: Vec<u32>,
    #[serde(rename = "uco-observable:sectionAlignment")]
    pub section_alignment: Vec<u32>,
    #[serde(rename = "uco-observable:sizeOfCode")]
    pub size_of_code: Vec<u32>,
    #[serde(rename = "uco-observable:sizeOfHeaders")]
    pub size_of_headers: Vec<u32>,
    #[serde(rename = "uco-observable:sizeOfHeapCommit")]
    pub size_of_heap_commit: Vec<u32>,
    #[serde(rename = "uco-observable:sizeOfHeapReserve")]
    pub size_of_heap_reserve: Vec<u32>,
    #[serde(rename = "uco-observable:sizeOfImage")]
    pub size_of_image: Vec<u32>,
    #[serde(rename = "uco-observable:sizeOfInitializedData")]
    pub size_of_initialized_data: Vec<u32>,
    #[serde(rename = "uco-observable:sizeOfStackCommit")]
    pub size_of_stack_commit: Vec<u32>,
    #[serde(rename = "uco-observable:sizeOfStackReserve")]
    pub size_of_stack_reserve: Vec<u32>,
    #[serde(rename = "uco-observable:sizeOfUninitializedData")]
    pub size_of_uninitialized_data: Vec<u32>,
    #[serde(rename = "uco-observable:subsystem")]
    pub subsystem: Vec<u16>,
    #[serde(rename = "uco-observable:win32VersionValue")]
    pub win32_version_value: Vec<u32>,
}

impl WindowsPEOptionalHeader {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPEOptionalHeader";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsPEOptionalHeaderBuilder {
        WindowsPEOptionalHeaderBuilder {
            address_of_entry_point: Vec::new(),
            base_of_code: Vec::new(),
            checksum: Vec::new(),
            dll_characteristics: Vec::new(),
            file_alignment: Vec::new(),
            image_base: Vec::new(),
            loader_flags: Vec::new(),
            magic: Vec::new(),
            major_image_version: Vec::new(),
            major_linker_version: Vec::new(),
            major_os_version: Vec::new(),
            major_subsystem_version: Vec::new(),
            minor_image_version: Vec::new(),
            minor_linker_version: Vec::new(),
            minor_os_version: Vec::new(),
            minor_subsystem_version: Vec::new(),
            number_of_rva_and_sizes: Vec::new(),
            section_alignment: Vec::new(),
            size_of_code: Vec::new(),
            size_of_headers: Vec::new(),
            size_of_heap_commit: Vec::new(),
            size_of_heap_reserve: Vec::new(),
            size_of_image: Vec::new(),
            size_of_initialized_data: Vec::new(),
            size_of_stack_commit: Vec::new(),
            size_of_stack_reserve: Vec::new(),
            size_of_uninitialized_data: Vec::new(),
            subsystem: Vec::new(),
            win32_version_value: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsPEOptionalHeaderBuilder {
    address_of_entry_point: Vec<u32>,
    base_of_code: Vec<u32>,
    checksum: Vec<u32>,
    dll_characteristics: Vec<u16>,
    file_alignment: Vec<u32>,
    image_base: Vec<u32>,
    loader_flags: Vec<u32>,
    magic: Vec<u16>,
    major_image_version: Vec<u16>,
    major_linker_version: Vec<i8>,
    major_os_version: Vec<u16>,
    major_subsystem_version: Vec<u16>,
    minor_image_version: Vec<u16>,
    minor_linker_version: Vec<i8>,
    minor_os_version: Vec<u16>,
    minor_subsystem_version: Vec<u16>,
    number_of_rva_and_sizes: Vec<u32>,
    section_alignment: Vec<u32>,
    size_of_code: Vec<u32>,
    size_of_headers: Vec<u32>,
    size_of_heap_commit: Vec<u32>,
    size_of_heap_reserve: Vec<u32>,
    size_of_image: Vec<u32>,
    size_of_initialized_data: Vec<u32>,
    size_of_stack_commit: Vec<u32>,
    size_of_stack_reserve: Vec<u32>,
    size_of_uninitialized_data: Vec<u32>,
    subsystem: Vec<u16>,
    win32_version_value: Vec<u32>,
}

impl WindowsPEOptionalHeaderBuilder {
    pub fn address_of_entry_point(mut self, value: Vec<u32>) -> Self {
        self.address_of_entry_point = value;
        self
    }

    pub fn base_of_code(mut self, value: Vec<u32>) -> Self {
        self.base_of_code = value;
        self
    }

    pub fn checksum(mut self, value: Vec<u32>) -> Self {
        self.checksum = value;
        self
    }

    pub fn dll_characteristics(mut self, value: Vec<u16>) -> Self {
        self.dll_characteristics = value;
        self
    }

    pub fn file_alignment(mut self, value: Vec<u32>) -> Self {
        self.file_alignment = value;
        self
    }

    pub fn image_base(mut self, value: Vec<u32>) -> Self {
        self.image_base = value;
        self
    }

    pub fn loader_flags(mut self, value: Vec<u32>) -> Self {
        self.loader_flags = value;
        self
    }

    pub fn magic(mut self, value: Vec<u16>) -> Self {
        self.magic = value;
        self
    }

    pub fn major_image_version(mut self, value: Vec<u16>) -> Self {
        self.major_image_version = value;
        self
    }

    pub fn major_linker_version(mut self, value: Vec<i8>) -> Self {
        self.major_linker_version = value;
        self
    }

    pub fn major_os_version(mut self, value: Vec<u16>) -> Self {
        self.major_os_version = value;
        self
    }

    pub fn major_subsystem_version(mut self, value: Vec<u16>) -> Self {
        self.major_subsystem_version = value;
        self
    }

    pub fn minor_image_version(mut self, value: Vec<u16>) -> Self {
        self.minor_image_version = value;
        self
    }

    pub fn minor_linker_version(mut self, value: Vec<i8>) -> Self {
        self.minor_linker_version = value;
        self
    }

    pub fn minor_os_version(mut self, value: Vec<u16>) -> Self {
        self.minor_os_version = value;
        self
    }

    pub fn minor_subsystem_version(mut self, value: Vec<u16>) -> Self {
        self.minor_subsystem_version = value;
        self
    }

    pub fn number_of_rva_and_sizes(mut self, value: Vec<u32>) -> Self {
        self.number_of_rva_and_sizes = value;
        self
    }

    pub fn section_alignment(mut self, value: Vec<u32>) -> Self {
        self.section_alignment = value;
        self
    }

    pub fn size_of_code(mut self, value: Vec<u32>) -> Self {
        self.size_of_code = value;
        self
    }

    pub fn size_of_headers(mut self, value: Vec<u32>) -> Self {
        self.size_of_headers = value;
        self
    }

    pub fn size_of_heap_commit(mut self, value: Vec<u32>) -> Self {
        self.size_of_heap_commit = value;
        self
    }

    pub fn size_of_heap_reserve(mut self, value: Vec<u32>) -> Self {
        self.size_of_heap_reserve = value;
        self
    }

    pub fn size_of_image(mut self, value: Vec<u32>) -> Self {
        self.size_of_image = value;
        self
    }

    pub fn size_of_initialized_data(mut self, value: Vec<u32>) -> Self {
        self.size_of_initialized_data = value;
        self
    }

    pub fn size_of_stack_commit(mut self, value: Vec<u32>) -> Self {
        self.size_of_stack_commit = value;
        self
    }

    pub fn size_of_stack_reserve(mut self, value: Vec<u32>) -> Self {
        self.size_of_stack_reserve = value;
        self
    }

    pub fn size_of_uninitialized_data(mut self, value: Vec<u32>) -> Self {
        self.size_of_uninitialized_data = value;
        self
    }

    pub fn subsystem(mut self, value: Vec<u16>) -> Self {
        self.subsystem = value;
        self
    }

    pub fn win32_version_value(mut self, value: Vec<u32>) -> Self {
        self.win32_version_value = value;
        self
    }

    pub fn build(self) -> WindowsPEOptionalHeader {
        WindowsPEOptionalHeader {
            class_iri: WindowsPEOptionalHeader::CLASS_IRI,
            address_of_entry_point: self.address_of_entry_point,
            base_of_code: self.base_of_code,
            checksum: self.checksum,
            dll_characteristics: self.dll_characteristics,
            file_alignment: self.file_alignment,
            image_base: self.image_base,
            loader_flags: self.loader_flags,
            magic: self.magic,
            major_image_version: self.major_image_version,
            major_linker_version: self.major_linker_version,
            major_os_version: self.major_os_version,
            major_subsystem_version: self.major_subsystem_version,
            minor_image_version: self.minor_image_version,
            minor_linker_version: self.minor_linker_version,
            minor_os_version: self.minor_os_version,
            minor_subsystem_version: self.minor_subsystem_version,
            number_of_rva_and_sizes: self.number_of_rva_and_sizes,
            section_alignment: self.section_alignment,
            size_of_code: self.size_of_code,
            size_of_headers: self.size_of_headers,
            size_of_heap_commit: self.size_of_heap_commit,
            size_of_heap_reserve: self.size_of_heap_reserve,
            size_of_image: self.size_of_image,
            size_of_initialized_data: self.size_of_initialized_data,
            size_of_stack_commit: self.size_of_stack_commit,
            size_of_stack_reserve: self.size_of_stack_reserve,
            size_of_uninitialized_data: self.size_of_uninitialized_data,
            subsystem: self.subsystem,
            win32_version_value: self.win32_version_value,
        }
    }
}

impl CaseObject for WindowsPEOptionalHeader {
    fn class_iri() -> &'static str { WindowsPEOptionalHeader::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsPEOptionalHeader" }
}

/// A Windows PE section is a grouping of characteristics unique to a specific default or custom-defined region of a Windows PE (Portable Executable) file, consisting of an individual portion of the actua
#[derive(Debug, Clone, Serialize)]
pub struct WindowsPESection {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:name")]
    pub name: Option<String>,
    #[serde(rename = "uco-observable:entropy")]
    pub entropy: Option<f64>,
    #[serde(rename = "uco-observable:hashes")]
    pub hashes: Vec<Hash>,
    #[serde(rename = "uco-observable:size")]
    pub size: Option<i64>,
}

impl WindowsPESection {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPESection";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsPESectionBuilder {
        WindowsPESectionBuilder {
            name: None,
            entropy: None,
            hashes: Vec::new(),
            size: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsPESectionBuilder {
    name: Option<String>,
    entropy: Option<f64>,
    hashes: Vec<Hash>,
    size: Option<i64>,
}

impl WindowsPESectionBuilder {
    pub fn name(mut self, value: String) -> Self {
        self.name = Some(value);
        self
    }

    pub fn entropy(mut self, value: f64) -> Self {
        self.entropy = Some(value);
        self
    }

    pub fn hashes(mut self, value: Vec<Hash>) -> Self {
        self.hashes = value;
        self
    }

    pub fn size(mut self, value: i64) -> Self {
        self.size = Some(value);
        self
    }

    pub fn build(self) -> WindowsPESection {
        WindowsPESection {
            class_iri: WindowsPESection::CLASS_IRI,
            name: self.name,
            entropy: self.entropy,
            hashes: self.hashes,
            size: self.size,
        }
    }
}

impl CaseObject for WindowsPESection {
    fn class_iri() -> &'static str { WindowsPESection::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsPESection" }
}

/// The Windows prefetch contains entries in a Windows prefetch file (used to speed up application startup starting with Windows XP).
#[derive(Debug, Clone, Serialize)]
pub struct WindowsPrefetch {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsPrefetch {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPrefetch";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsPrefetchBuilder {
        WindowsPrefetchBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsPrefetchBuilder {
}

impl WindowsPrefetchBuilder {
    pub fn build(self) -> WindowsPrefetch {
        WindowsPrefetch {
            class_iri: WindowsPrefetch::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsPrefetch {
    fn class_iri() -> &'static str { WindowsPrefetch::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsPrefetch" }
}

/// A Windows prefetch facet is a grouping of characteristics unique to entries in the Windows prefetch file (used to speed up application startup starting with Windows XP).
#[derive(Debug, Clone, Serialize)]
pub struct WindowsPrefetchFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:accessedDirectory")]
    pub accessed_directory: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:accessedFile")]
    pub accessed_file: Vec<ObservableObject>,
    #[serde(rename = "uco-observable:applicationFileName")]
    pub application_file_name: Option<String>,
    #[serde(rename = "uco-observable:firstRun")]
    pub first_run: Option<String>,
    #[serde(rename = "uco-observable:lastRun")]
    pub last_run: Option<String>,
    #[serde(rename = "uco-observable:prefetchHash")]
    pub prefetch_hash: Option<String>,
    #[serde(rename = "uco-observable:timesExecuted")]
    pub times_executed: Option<i64>,
    #[serde(rename = "uco-observable:volume")]
    pub volume: Option<ObservableObject>,
}

impl WindowsPrefetchFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsPrefetchFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsPrefetchFacetBuilder {
        WindowsPrefetchFacetBuilder {
            accessed_directory: Vec::new(),
            accessed_file: Vec::new(),
            application_file_name: None,
            first_run: None,
            last_run: None,
            prefetch_hash: None,
            times_executed: None,
            volume: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsPrefetchFacetBuilder {
    accessed_directory: Vec<ObservableObject>,
    accessed_file: Vec<ObservableObject>,
    application_file_name: Option<String>,
    first_run: Option<String>,
    last_run: Option<String>,
    prefetch_hash: Option<String>,
    times_executed: Option<i64>,
    volume: Option<ObservableObject>,
}

impl WindowsPrefetchFacetBuilder {
    pub fn accessed_directory(mut self, value: Vec<ObservableObject>) -> Self {
        self.accessed_directory = value;
        self
    }

    pub fn accessed_file(mut self, value: Vec<ObservableObject>) -> Self {
        self.accessed_file = value;
        self
    }

    pub fn application_file_name(mut self, value: String) -> Self {
        self.application_file_name = Some(value);
        self
    }

    pub fn first_run(mut self, value: String) -> Self {
        self.first_run = Some(value);
        self
    }

    pub fn last_run(mut self, value: String) -> Self {
        self.last_run = Some(value);
        self
    }

    pub fn prefetch_hash(mut self, value: String) -> Self {
        self.prefetch_hash = Some(value);
        self
    }

    pub fn times_executed(mut self, value: i64) -> Self {
        self.times_executed = Some(value);
        self
    }

    pub fn volume(mut self, value: ObservableObject) -> Self {
        self.volume = Some(value);
        self
    }

    pub fn build(self) -> WindowsPrefetchFacet {
        WindowsPrefetchFacet {
            class_iri: WindowsPrefetchFacet::CLASS_IRI,
            accessed_directory: self.accessed_directory,
            accessed_file: self.accessed_file,
            application_file_name: self.application_file_name,
            first_run: self.first_run,
            last_run: self.last_run,
            prefetch_hash: self.prefetch_hash,
            times_executed: self.times_executed,
            volume: self.volume,
        }
    }
}

impl CaseObject for WindowsPrefetchFacet {
    fn class_iri() -> &'static str { WindowsPrefetchFacet::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsPrefetchFacet" }
}

/// A Windows process is a program running on a Windows operating system.
#[derive(Debug, Clone, Serialize)]
pub struct WindowsProcess {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsProcess {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsProcess";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsProcessBuilder {
        WindowsProcessBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsProcessBuilder {
}

impl WindowsProcessBuilder {
    pub fn build(self) -> WindowsProcess {
        WindowsProcess {
            class_iri: WindowsProcess::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsProcess {
    fn class_iri() -> &'static str { WindowsProcess::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsProcess" }
}

/// A Windows process facet is a grouping of characteristics unique to a program running on a Windows operating system.
#[derive(Debug, Clone, Serialize)]
pub struct WindowsProcessFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:aslrEnabled")]
    pub aslr_enabled: Option<bool>,
    #[serde(rename = "uco-observable:depEnabled")]
    pub dep_enabled: Option<bool>,
    #[serde(rename = "uco-observable:ownerSID")]
    pub owner_sid: Option<String>,
    #[serde(rename = "uco-observable:priority")]
    pub priority: Option<String>,
    #[serde(rename = "uco-observable:startupInfo")]
    pub startup_info: Option<Dictionary>,
    #[serde(rename = "uco-observable:windowTitle")]
    pub window_title: Option<String>,
}

impl WindowsProcessFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsProcessFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsProcessFacetBuilder {
        WindowsProcessFacetBuilder {
            aslr_enabled: None,
            dep_enabled: None,
            owner_sid: None,
            priority: None,
            startup_info: None,
            window_title: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsProcessFacetBuilder {
    aslr_enabled: Option<bool>,
    dep_enabled: Option<bool>,
    owner_sid: Option<String>,
    priority: Option<String>,
    startup_info: Option<Dictionary>,
    window_title: Option<String>,
}

impl WindowsProcessFacetBuilder {
    pub fn aslr_enabled(mut self, value: bool) -> Self {
        self.aslr_enabled = Some(value);
        self
    }

    pub fn dep_enabled(mut self, value: bool) -> Self {
        self.dep_enabled = Some(value);
        self
    }

    pub fn owner_sid(mut self, value: String) -> Self {
        self.owner_sid = Some(value);
        self
    }

    pub fn priority(mut self, value: String) -> Self {
        self.priority = Some(value);
        self
    }

    pub fn startup_info(mut self, value: Dictionary) -> Self {
        self.startup_info = Some(value);
        self
    }

    pub fn window_title(mut self, value: String) -> Self {
        self.window_title = Some(value);
        self
    }

    pub fn build(self) -> WindowsProcessFacet {
        WindowsProcessFacet {
            class_iri: WindowsProcessFacet::CLASS_IRI,
            aslr_enabled: self.aslr_enabled,
            dep_enabled: self.dep_enabled,
            owner_sid: self.owner_sid,
            priority: self.priority,
            startup_info: self.startup_info,
            window_title: self.window_title,
        }
    }
}

impl CaseObject for WindowsProcessFacet {
    fn class_iri() -> &'static str { WindowsProcessFacet::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsProcessFacet" }
}

/// The Windows registry hive is a particular logical group of keys, subkeys, and values in a Windows registry (a hierarchical database that stores low-level settings for the Microsoft Windows operating s
#[derive(Debug, Clone, Serialize)]
pub struct WindowsRegistryHive {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsRegistryHive {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryHive";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsRegistryHiveBuilder {
        WindowsRegistryHiveBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsRegistryHiveBuilder {
}

impl WindowsRegistryHiveBuilder {
    pub fn build(self) -> WindowsRegistryHive {
        WindowsRegistryHive {
            class_iri: WindowsRegistryHive::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsRegistryHive {
    fn class_iri() -> &'static str { WindowsRegistryHive::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsRegistryHive" }
}

/// A Windows registry hive facet is a grouping of characteristics unique to a particular logical group of keys, subkeys, and values in a Windows registry (a hierarchical database that stores low-level se
#[derive(Debug, Clone, Serialize)]
pub struct WindowsRegistryHiveFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:hiveType")]
    pub hive_type: Option<String>,
}

impl WindowsRegistryHiveFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryHiveFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsRegistryHiveFacetBuilder {
        WindowsRegistryHiveFacetBuilder {
            hive_type: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsRegistryHiveFacetBuilder {
    hive_type: Option<String>,
}

impl WindowsRegistryHiveFacetBuilder {
    pub fn hive_type(mut self, value: String) -> Self {
        self.hive_type = Some(value);
        self
    }

    pub fn build(self) -> WindowsRegistryHiveFacet {
        WindowsRegistryHiveFacet {
            class_iri: WindowsRegistryHiveFacet::CLASS_IRI,
            hive_type: self.hive_type,
        }
    }
}

impl CaseObject for WindowsRegistryHiveFacet {
    fn class_iri() -> &'static str { WindowsRegistryHiveFacet::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsRegistryHiveFacet" }
}

/// A Windows registry key is a particular key within a Windows registry (a hierarchical database that stores low-level settings for the Microsoft Windows operating system and for applications that opt to
#[derive(Debug, Clone, Serialize)]
pub struct WindowsRegistryKey {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsRegistryKey {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryKey";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsRegistryKeyBuilder {
        WindowsRegistryKeyBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsRegistryKeyBuilder {
}

impl WindowsRegistryKeyBuilder {
    pub fn build(self) -> WindowsRegistryKey {
        WindowsRegistryKey {
            class_iri: WindowsRegistryKey::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsRegistryKey {
    fn class_iri() -> &'static str { WindowsRegistryKey::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsRegistryKey" }
}

/// A Windows registry key facet is a grouping of characteristics unique to a particular key within a Windows registry (A hierarchical database that stores low-level settings for the Microsoft Windows ope
#[derive(Debug, Clone, Serialize)]
pub struct WindowsRegistryKeyFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:creator")]
    pub creator: Option<ObservableObject>,
    #[serde(rename = "uco-observable:key")]
    pub key: Option<String>,
    #[serde(rename = "uco-observable:modifiedTime")]
    pub modified_time: Option<String>,
    #[serde(rename = "uco-observable:numberOfSubkeys")]
    pub number_of_subkeys: Option<i64>,
    #[serde(rename = "uco-observable:registryValues")]
    pub registry_values: Vec<WindowsRegistryValue>,
}

impl WindowsRegistryKeyFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryKeyFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsRegistryKeyFacetBuilder {
        WindowsRegistryKeyFacetBuilder {
            creator: None,
            key: None,
            modified_time: None,
            number_of_subkeys: None,
            registry_values: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsRegistryKeyFacetBuilder {
    creator: Option<ObservableObject>,
    key: Option<String>,
    modified_time: Option<String>,
    number_of_subkeys: Option<i64>,
    registry_values: Vec<WindowsRegistryValue>,
}

impl WindowsRegistryKeyFacetBuilder {
    pub fn creator(mut self, value: ObservableObject) -> Self {
        self.creator = Some(value);
        self
    }

    pub fn key(mut self, value: String) -> Self {
        self.key = Some(value);
        self
    }

    pub fn modified_time(mut self, value: String) -> Self {
        self.modified_time = Some(value);
        self
    }

    pub fn number_of_subkeys(mut self, value: i64) -> Self {
        self.number_of_subkeys = Some(value);
        self
    }

    pub fn registry_values(mut self, value: Vec<WindowsRegistryValue>) -> Self {
        self.registry_values = value;
        self
    }

    pub fn build(self) -> WindowsRegistryKeyFacet {
        WindowsRegistryKeyFacet {
            class_iri: WindowsRegistryKeyFacet::CLASS_IRI,
            creator: self.creator,
            key: self.key,
            modified_time: self.modified_time,
            number_of_subkeys: self.number_of_subkeys,
            registry_values: self.registry_values,
        }
    }
}

impl CaseObject for WindowsRegistryKeyFacet {
    fn class_iri() -> &'static str { WindowsRegistryKeyFacet::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsRegistryKeyFacet" }
}

/// A Windows registry value is a grouping of characteristics unique to a particular value within a Windows registry (a hierarchical database that stores low-level settings for the Microsoft Windows opera
#[derive(Debug, Clone, Serialize)]
pub struct WindowsRegistryValue {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-core:name")]
    pub name: Option<String>,
    #[serde(rename = "uco-observable:data")]
    pub data: Option<String>,
    #[serde(rename = "uco-observable:dataType")]
    pub data_type: Option<String>,
}

impl WindowsRegistryValue {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsRegistryValue";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsRegistryValueBuilder {
        WindowsRegistryValueBuilder {
            name: None,
            data: None,
            data_type: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsRegistryValueBuilder {
    name: Option<String>,
    data: Option<String>,
    data_type: Option<String>,
}

impl WindowsRegistryValueBuilder {
    pub fn name(mut self, value: String) -> Self {
        self.name = Some(value);
        self
    }

    pub fn data(mut self, value: String) -> Self {
        self.data = Some(value);
        self
    }

    pub fn data_type(mut self, value: String) -> Self {
        self.data_type = Some(value);
        self
    }

    pub fn build(self) -> WindowsRegistryValue {
        WindowsRegistryValue {
            class_iri: WindowsRegistryValue::CLASS_IRI,
            name: self.name,
            data: self.data,
            data_type: self.data_type,
        }
    }
}

impl CaseObject for WindowsRegistryValue {
    fn class_iri() -> &'static str { WindowsRegistryValue::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsRegistryValue" }
}

/// A Windows service is a specific Windows service (a computer program that operates in the background of a Windows operating system, similar to the way a UNIX daemon runs on UNIX). [based on https://en.
#[derive(Debug, Clone, Serialize)]
pub struct WindowsService {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsService {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsService";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsServiceBuilder {
        WindowsServiceBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsServiceBuilder {
}

impl WindowsServiceBuilder {
    pub fn build(self) -> WindowsService {
        WindowsService {
            class_iri: WindowsService::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsService {
    fn class_iri() -> &'static str { WindowsService::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsService" }
}

/// A Windows service facet is a grouping of characteristics unique to a specific Windows service (a computer program that operates in the background of a Windows operating system, similar to the way a UN
#[derive(Debug, Clone, Serialize)]
pub struct WindowsServiceFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:descriptions")]
    pub descriptions: Vec<String>,
    #[serde(rename = "uco-observable:displayName")]
    pub display_name: Option<String>,
    #[serde(rename = "uco-observable:groupName")]
    pub group_name: Option<String>,
    #[serde(rename = "uco-observable:serviceName")]
    pub service_name: Option<String>,
    #[serde(rename = "uco-observable:serviceStatus")]
    pub service_status: Option<String>,
    #[serde(rename = "uco-observable:serviceType")]
    pub service_type: Option<String>,
    #[serde(rename = "uco-observable:startCommandLine")]
    pub start_command_line: Option<String>,
    #[serde(rename = "uco-observable:startType")]
    pub start_type: Option<String>,
}

impl WindowsServiceFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsServiceFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsServiceFacetBuilder {
        WindowsServiceFacetBuilder {
            descriptions: Vec::new(),
            display_name: None,
            group_name: None,
            service_name: None,
            service_status: None,
            service_type: None,
            start_command_line: None,
            start_type: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsServiceFacetBuilder {
    descriptions: Vec<String>,
    display_name: Option<String>,
    group_name: Option<String>,
    service_name: Option<String>,
    service_status: Option<String>,
    service_type: Option<String>,
    start_command_line: Option<String>,
    start_type: Option<String>,
}

impl WindowsServiceFacetBuilder {
    pub fn descriptions(mut self, value: Vec<String>) -> Self {
        self.descriptions = value;
        self
    }

    pub fn display_name(mut self, value: String) -> Self {
        self.display_name = Some(value);
        self
    }

    pub fn group_name(mut self, value: String) -> Self {
        self.group_name = Some(value);
        self
    }

    pub fn service_name(mut self, value: String) -> Self {
        self.service_name = Some(value);
        self
    }

    pub fn service_status(mut self, value: String) -> Self {
        self.service_status = Some(value);
        self
    }

    pub fn service_type(mut self, value: String) -> Self {
        self.service_type = Some(value);
        self
    }

    pub fn start_command_line(mut self, value: String) -> Self {
        self.start_command_line = Some(value);
        self
    }

    pub fn start_type(mut self, value: String) -> Self {
        self.start_type = Some(value);
        self
    }

    pub fn build(self) -> WindowsServiceFacet {
        WindowsServiceFacet {
            class_iri: WindowsServiceFacet::CLASS_IRI,
            descriptions: self.descriptions,
            display_name: self.display_name,
            group_name: self.group_name,
            service_name: self.service_name,
            service_status: self.service_status,
            service_type: self.service_type,
            start_command_line: self.start_command_line,
            start_type: self.start_type,
        }
    }
}

impl CaseObject for WindowsServiceFacet {
    fn class_iri() -> &'static str { WindowsServiceFacet::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsServiceFacet" }
}

/// A Windows system restore is a capture of a Windows computer's state (including system files, installed applications, Windows Registry, and system settings) at a particular point in time such that the 
#[derive(Debug, Clone, Serialize)]
pub struct WindowsSystemRestore {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsSystemRestore {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsSystemRestore";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsSystemRestoreBuilder {
        WindowsSystemRestoreBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsSystemRestoreBuilder {
}

impl WindowsSystemRestoreBuilder {
    pub fn build(self) -> WindowsSystemRestore {
        WindowsSystemRestore {
            class_iri: WindowsSystemRestore::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsSystemRestore {
    fn class_iri() -> &'static str { WindowsSystemRestore::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsSystemRestore" }
}

/// A Windows task is a process that is scheduled to execute on a Windows operating system by the Windows Task Scheduler. [based on http://msdn.microsoft.com/en-us/library/windows/desktop/aa381311(v=vs.85
#[derive(Debug, Clone, Serialize)]
pub struct WindowsTask {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsTask {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsTask";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsTaskBuilder {
        WindowsTaskBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsTaskBuilder {
}

impl WindowsTaskBuilder {
    pub fn build(self) -> WindowsTask {
        WindowsTask {
            class_iri: WindowsTask::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsTask {
    fn class_iri() -> &'static str { WindowsTask::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsTask" }
}

/// A Windows Task facet is a grouping of characteristics unique to a Windows Task (a process that is scheduled to execute on a Windows operating system by the Windows Task Scheduler). [based on http://ms
#[derive(Debug, Clone, Serialize)]
pub struct WindowsTaskFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:account")]
    pub account: Option<ObservableObject>,
    #[serde(rename = "uco-observable:accountLogonType")]
    pub account_logon_type: Option<String>,
    #[serde(rename = "uco-observable:accountRunLevel")]
    pub account_run_level: Option<String>,
    #[serde(rename = "uco-observable:actionList")]
    pub action_list: Vec<TaskActionType>,
    #[serde(rename = "uco-observable:application")]
    pub application: Option<ObservableObject>,
    #[serde(rename = "uco-observable:exitCode")]
    pub exit_code: Option<i64>,
    #[serde(rename = "uco-observable:flags")]
    pub flags: Vec<String>,
    #[serde(rename = "uco-observable:imageName")]
    pub image_name: Option<String>,
    #[serde(rename = "uco-observable:maxRunTime")]
    pub max_run_time: Option<i64>,
    #[serde(rename = "uco-observable:mostRecentRunTime")]
    pub most_recent_run_time: Option<String>,
    #[serde(rename = "uco-observable:nextRunTime")]
    pub next_run_time: Option<String>,
    #[serde(rename = "uco-observable:observableCreatedTime")]
    pub observable_created_time: Option<String>,
    #[serde(rename = "uco-observable:parameters")]
    pub parameters: Option<String>,
    #[serde(rename = "uco-observable:priority")]
    pub priority: Vec<serde_json::Value>,
    #[serde(rename = "uco-observable:status")]
    pub status: Vec<String>,
    #[serde(rename = "uco-observable:taskComment")]
    pub task_comment: Option<String>,
    #[serde(rename = "uco-observable:taskCreator")]
    pub task_creator: Option<String>,
    #[serde(rename = "uco-observable:triggerList")]
    pub trigger_list: Vec<TriggerType>,
    #[serde(rename = "uco-observable:workItemData")]
    pub work_item_data: Option<ObservableObject>,
    #[serde(rename = "uco-observable:workingDirectory")]
    pub working_directory: Option<ObservableObject>,
}

impl WindowsTaskFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsTaskFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsTaskFacetBuilder {
        WindowsTaskFacetBuilder {
            account: None,
            account_logon_type: None,
            account_run_level: None,
            action_list: Vec::new(),
            application: None,
            exit_code: None,
            flags: Vec::new(),
            image_name: None,
            max_run_time: None,
            most_recent_run_time: None,
            next_run_time: None,
            observable_created_time: None,
            parameters: None,
            priority: Vec::new(),
            status: Vec::new(),
            task_comment: None,
            task_creator: None,
            trigger_list: Vec::new(),
            work_item_data: None,
            working_directory: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsTaskFacetBuilder {
    account: Option<ObservableObject>,
    account_logon_type: Option<String>,
    account_run_level: Option<String>,
    action_list: Vec<TaskActionType>,
    application: Option<ObservableObject>,
    exit_code: Option<i64>,
    flags: Vec<String>,
    image_name: Option<String>,
    max_run_time: Option<i64>,
    most_recent_run_time: Option<String>,
    next_run_time: Option<String>,
    observable_created_time: Option<String>,
    parameters: Option<String>,
    priority: Vec<serde_json::Value>,
    status: Vec<String>,
    task_comment: Option<String>,
    task_creator: Option<String>,
    trigger_list: Vec<TriggerType>,
    work_item_data: Option<ObservableObject>,
    working_directory: Option<ObservableObject>,
}

impl WindowsTaskFacetBuilder {
    pub fn account(mut self, value: ObservableObject) -> Self {
        self.account = Some(value);
        self
    }

    pub fn account_logon_type(mut self, value: String) -> Self {
        self.account_logon_type = Some(value);
        self
    }

    pub fn account_run_level(mut self, value: String) -> Self {
        self.account_run_level = Some(value);
        self
    }

    pub fn action_list(mut self, value: Vec<TaskActionType>) -> Self {
        self.action_list = value;
        self
    }

    pub fn application(mut self, value: ObservableObject) -> Self {
        self.application = Some(value);
        self
    }

    pub fn exit_code(mut self, value: i64) -> Self {
        self.exit_code = Some(value);
        self
    }

    pub fn flags(mut self, value: Vec<String>) -> Self {
        self.flags = value;
        self
    }

    pub fn image_name(mut self, value: String) -> Self {
        self.image_name = Some(value);
        self
    }

    pub fn max_run_time(mut self, value: i64) -> Self {
        self.max_run_time = Some(value);
        self
    }

    pub fn most_recent_run_time(mut self, value: String) -> Self {
        self.most_recent_run_time = Some(value);
        self
    }

    pub fn next_run_time(mut self, value: String) -> Self {
        self.next_run_time = Some(value);
        self
    }

    pub fn observable_created_time(mut self, value: String) -> Self {
        self.observable_created_time = Some(value);
        self
    }

    pub fn parameters(mut self, value: String) -> Self {
        self.parameters = Some(value);
        self
    }

    pub fn priority(mut self, value: Vec<serde_json::Value>) -> Self {
        self.priority = value;
        self
    }

    pub fn status(mut self, value: Vec<String>) -> Self {
        self.status = value;
        self
    }

    pub fn task_comment(mut self, value: String) -> Self {
        self.task_comment = Some(value);
        self
    }

    pub fn task_creator(mut self, value: String) -> Self {
        self.task_creator = Some(value);
        self
    }

    pub fn trigger_list(mut self, value: Vec<TriggerType>) -> Self {
        self.trigger_list = value;
        self
    }

    pub fn work_item_data(mut self, value: ObservableObject) -> Self {
        self.work_item_data = Some(value);
        self
    }

    pub fn working_directory(mut self, value: ObservableObject) -> Self {
        self.working_directory = Some(value);
        self
    }

    pub fn build(self) -> WindowsTaskFacet {
        WindowsTaskFacet {
            class_iri: WindowsTaskFacet::CLASS_IRI,
            account: self.account,
            account_logon_type: self.account_logon_type,
            account_run_level: self.account_run_level,
            action_list: self.action_list,
            application: self.application,
            exit_code: self.exit_code,
            flags: self.flags,
            image_name: self.image_name,
            max_run_time: self.max_run_time,
            most_recent_run_time: self.most_recent_run_time,
            next_run_time: self.next_run_time,
            observable_created_time: self.observable_created_time,
            parameters: self.parameters,
            priority: self.priority,
            status: self.status,
            task_comment: self.task_comment,
            task_creator: self.task_creator,
            trigger_list: self.trigger_list,
            work_item_data: self.work_item_data,
            working_directory: self.working_directory,
        }
    }
}

impl CaseObject for WindowsTaskFacet {
    fn class_iri() -> &'static str { WindowsTaskFacet::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsTaskFacet" }
}

/// A Windows thread is a single thread of execution within a Windows process.
#[derive(Debug, Clone, Serialize)]
pub struct WindowsThread {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsThread {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsThread";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsThreadBuilder {
        WindowsThreadBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsThreadBuilder {
}

impl WindowsThreadBuilder {
    pub fn build(self) -> WindowsThread {
        WindowsThread {
            class_iri: WindowsThread::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsThread {
    fn class_iri() -> &'static str { WindowsThread::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsThread" }
}

/// A Windows thread facet is a grouping os characteristics unique to a single thread of execution within a Windows process.
#[derive(Debug, Clone, Serialize)]
pub struct WindowsThreadFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:context")]
    pub context: Option<String>,
    #[serde(rename = "uco-observable:creationFlags")]
    pub creation_flags: Vec<u32>,
    #[serde(rename = "uco-observable:creationTime")]
    pub creation_time: Option<String>,
    #[serde(rename = "uco-observable:observableCreatedTime")]
    pub observable_created_time: Option<String>,
    #[serde(rename = "uco-observable:parameterAddress")]
    pub parameter_address: Vec<Vec<u8>>,
    #[serde(rename = "uco-observable:priority")]
    pub priority: Option<i64>,
    #[serde(rename = "uco-observable:runningStatus")]
    pub running_status: Option<String>,
    #[serde(rename = "uco-observable:securityAttributes")]
    pub security_attributes: Option<String>,
    #[serde(rename = "uco-observable:stackSize")]
    pub stack_size: Vec<u64>,
    #[serde(rename = "uco-observable:startAddress")]
    pub start_address: Vec<Vec<u8>>,
    #[serde(rename = "uco-observable:threadID")]
    pub thread_id: Vec<u64>,
}

impl WindowsThreadFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsThreadFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsThreadFacetBuilder {
        WindowsThreadFacetBuilder {
            context: None,
            creation_flags: Vec::new(),
            creation_time: None,
            observable_created_time: None,
            parameter_address: Vec::new(),
            priority: None,
            running_status: None,
            security_attributes: None,
            stack_size: Vec::new(),
            start_address: Vec::new(),
            thread_id: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsThreadFacetBuilder {
    context: Option<String>,
    creation_flags: Vec<u32>,
    creation_time: Option<String>,
    observable_created_time: Option<String>,
    parameter_address: Vec<Vec<u8>>,
    priority: Option<i64>,
    running_status: Option<String>,
    security_attributes: Option<String>,
    stack_size: Vec<u64>,
    start_address: Vec<Vec<u8>>,
    thread_id: Vec<u64>,
}

impl WindowsThreadFacetBuilder {
    pub fn context(mut self, value: String) -> Self {
        self.context = Some(value);
        self
    }

    pub fn creation_flags(mut self, value: Vec<u32>) -> Self {
        self.creation_flags = value;
        self
    }

    pub fn creation_time(mut self, value: String) -> Self {
        self.creation_time = Some(value);
        self
    }

    pub fn observable_created_time(mut self, value: String) -> Self {
        self.observable_created_time = Some(value);
        self
    }

    pub fn parameter_address(mut self, value: Vec<Vec<u8>>) -> Self {
        self.parameter_address = value;
        self
    }

    pub fn priority(mut self, value: i64) -> Self {
        self.priority = Some(value);
        self
    }

    pub fn running_status(mut self, value: String) -> Self {
        self.running_status = Some(value);
        self
    }

    pub fn security_attributes(mut self, value: String) -> Self {
        self.security_attributes = Some(value);
        self
    }

    pub fn stack_size(mut self, value: Vec<u64>) -> Self {
        self.stack_size = value;
        self
    }

    pub fn start_address(mut self, value: Vec<Vec<u8>>) -> Self {
        self.start_address = value;
        self
    }

    pub fn thread_id(mut self, value: Vec<u64>) -> Self {
        self.thread_id = value;
        self
    }

    pub fn build(self) -> WindowsThreadFacet {
        WindowsThreadFacet {
            class_iri: WindowsThreadFacet::CLASS_IRI,
            context: self.context,
            creation_flags: self.creation_flags,
            creation_time: self.creation_time,
            observable_created_time: self.observable_created_time,
            parameter_address: self.parameter_address,
            priority: self.priority,
            running_status: self.running_status,
            security_attributes: self.security_attributes,
            stack_size: self.stack_size,
            start_address: self.start_address,
            thread_id: self.thread_id,
        }
    }
}

impl CaseObject for WindowsThreadFacet {
    fn class_iri() -> &'static str { WindowsThreadFacet::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsThreadFacet" }
}

/// A Windows volume facet is a grouping of characteristics unique to a single accessible storage area (volume) with a single Windows file system. [based on https://en.wikipedia.org/wiki/Volume_(computing
#[derive(Debug, Clone, Serialize)]
pub struct WindowsVolumeFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:driveLetter")]
    pub drive_letter: Option<String>,
    #[serde(rename = "uco-observable:driveType")]
    pub drive_type: Vec<String>,
    #[serde(rename = "uco-observable:windowsVolumeAttributes")]
    pub windows_volume_attributes: Vec<WindowsVolumeAttributeVocab>,
}

impl WindowsVolumeFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsVolumeFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsVolumeFacetBuilder {
        WindowsVolumeFacetBuilder {
            drive_letter: None,
            drive_type: Vec::new(),
            windows_volume_attributes: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsVolumeFacetBuilder {
    drive_letter: Option<String>,
    drive_type: Vec<String>,
    windows_volume_attributes: Vec<WindowsVolumeAttributeVocab>,
}

impl WindowsVolumeFacetBuilder {
    pub fn drive_letter(mut self, value: String) -> Self {
        self.drive_letter = Some(value);
        self
    }

    pub fn drive_type(mut self, value: Vec<String>) -> Self {
        self.drive_type = value;
        self
    }

    pub fn windows_volume_attributes(mut self, value: Vec<WindowsVolumeAttributeVocab>) -> Self {
        self.windows_volume_attributes = value;
        self
    }

    pub fn build(self) -> WindowsVolumeFacet {
        WindowsVolumeFacet {
            class_iri: WindowsVolumeFacet::CLASS_IRI,
            drive_letter: self.drive_letter,
            drive_type: self.drive_type,
            windows_volume_attributes: self.windows_volume_attributes,
        }
    }
}

impl CaseObject for WindowsVolumeFacet {
    fn class_iri() -> &'static str { WindowsVolumeFacet::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsVolumeFacet" }
}

/// A Windows waitable timer is a synchronization object within the Windows operating system whose state is set to signaled when a specified due time arrives. There are two types of waitable timers that c
#[derive(Debug, Clone, Serialize)]
pub struct WindowsWaitableTime {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WindowsWaitableTime {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsWaitableTime";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WindowsWaitableTimeBuilder {
        WindowsWaitableTimeBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WindowsWaitableTimeBuilder {
}

impl WindowsWaitableTimeBuilder {
    pub fn build(self) -> WindowsWaitableTime {
        WindowsWaitableTime {
            class_iri: WindowsWaitableTime::CLASS_IRI,
        }
    }
}

impl CaseObject for WindowsWaitableTime {
    fn class_iri() -> &'static str { WindowsWaitableTime::CLASS_IRI }
    fn type_name() -> &'static str { "WindowsWaitableTime" }
}

/// A wireless network connection is a connection (completed or attempted) across an IEEE 802.11 standards-confromant digital network (a group of two or more computer systems linked together). [based on h
#[derive(Debug, Clone, Serialize)]
pub struct WirelessNetworkConnection {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WirelessNetworkConnection {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WirelessNetworkConnection";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WirelessNetworkConnectionBuilder {
        WirelessNetworkConnectionBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WirelessNetworkConnectionBuilder {
}

impl WirelessNetworkConnectionBuilder {
    pub fn build(self) -> WirelessNetworkConnection {
        WirelessNetworkConnection {
            class_iri: WirelessNetworkConnection::CLASS_IRI,
        }
    }
}

impl CaseObject for WirelessNetworkConnection {
    fn class_iri() -> &'static str { WirelessNetworkConnection::CLASS_IRI }
    fn type_name() -> &'static str { "WirelessNetworkConnection" }
}

/// A wireless network connection facet is a grouping of characteristics unique to a connection (completed or attempted) across an IEEE 802.11 standards-conformant digital network (a group of two or more 
#[derive(Debug, Clone, Serialize)]
pub struct WirelessNetworkConnectionFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:baseStation")]
    pub base_station: Option<String>,
    #[serde(rename = "uco-observable:password")]
    pub password: Option<String>,
    #[serde(rename = "uco-observable:ssid")]
    pub ssid: Option<String>,
    #[serde(rename = "uco-observable:wirelessNetworkSecurityMode")]
    pub wireless_network_security_mode: Vec<String>,
}

impl WirelessNetworkConnectionFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WirelessNetworkConnectionFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WirelessNetworkConnectionFacetBuilder {
        WirelessNetworkConnectionFacetBuilder {
            base_station: None,
            password: None,
            ssid: None,
            wireless_network_security_mode: Vec::new(),
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WirelessNetworkConnectionFacetBuilder {
    base_station: Option<String>,
    password: Option<String>,
    ssid: Option<String>,
    wireless_network_security_mode: Vec<String>,
}

impl WirelessNetworkConnectionFacetBuilder {
    pub fn base_station(mut self, value: String) -> Self {
        self.base_station = Some(value);
        self
    }

    pub fn password(mut self, value: String) -> Self {
        self.password = Some(value);
        self
    }

    pub fn ssid(mut self, value: String) -> Self {
        self.ssid = Some(value);
        self
    }

    pub fn wireless_network_security_mode(mut self, value: Vec<String>) -> Self {
        self.wireless_network_security_mode = value;
        self
    }

    pub fn build(self) -> WirelessNetworkConnectionFacet {
        WirelessNetworkConnectionFacet {
            class_iri: WirelessNetworkConnectionFacet::CLASS_IRI,
            base_station: self.base_station,
            password: self.password,
            ssid: self.ssid,
            wireless_network_security_mode: self.wireless_network_security_mode,
        }
    }
}

impl CaseObject for WirelessNetworkConnectionFacet {
    fn class_iri() -> &'static str { WirelessNetworkConnectionFacet::CLASS_IRI }
    fn type_name() -> &'static str { "WirelessNetworkConnectionFacet" }
}

/// A write blocker is a device that allows read-only access to storage mediums in order to preserve the integrity of the data being analyzed. Examples include Tableau, Cellibrite, Talon, etc.
#[derive(Debug, Clone, Serialize)]
pub struct WriteBlocker {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl WriteBlocker {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/WriteBlocker";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> WriteBlockerBuilder {
        WriteBlockerBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct WriteBlockerBuilder {
}

impl WriteBlockerBuilder {
    pub fn build(self) -> WriteBlocker {
        WriteBlocker {
            class_iri: WriteBlocker::CLASS_IRI,
        }
    }
}

impl CaseObject for WriteBlocker {
    fn class_iri() -> &'static str { WriteBlocker::CLASS_IRI }
    fn type_name() -> &'static str { "WriteBlocker" }
}

/// A X.509 certificate is a public key digital identity certificate conformant to the X.509 PKI (Public Key Infrastructure) standard.
#[derive(Debug, Clone, Serialize)]
pub struct X509Certificate {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl X509Certificate {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/X509Certificate";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> X509CertificateBuilder {
        X509CertificateBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct X509CertificateBuilder {
}

impl X509CertificateBuilder {
    pub fn build(self) -> X509Certificate {
        X509Certificate {
            class_iri: X509Certificate::CLASS_IRI,
        }
    }
}

impl CaseObject for X509Certificate {
    fn class_iri() -> &'static str { X509Certificate::CLASS_IRI }
    fn type_name() -> &'static str { "X509Certificate" }
}

/// A X.509 certificate facet is a grouping of characteristics unique to a public key digital identity certificate conformant to the X.509 PKI (Public Key Infrastructure) standard. 
#[derive(Debug, Clone, Serialize)]
pub struct X509CertificateFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:isSelfSigned")]
    pub is_self_signed: Option<bool>,
    #[serde(rename = "uco-observable:issuer")]
    pub issuer: Option<String>,
    #[serde(rename = "uco-observable:issuerHash")]
    pub issuer_hash: Option<Hash>,
    #[serde(rename = "uco-observable:serialNumber")]
    pub serial_number: Option<String>,
    #[serde(rename = "uco-observable:signature")]
    pub signature: Option<String>,
    #[serde(rename = "uco-observable:signatureAlgorithm")]
    pub signature_algorithm: Option<String>,
    #[serde(rename = "uco-observable:subject")]
    pub subject: Option<String>,
    #[serde(rename = "uco-observable:subjectHash")]
    pub subject_hash: Option<Hash>,
    #[serde(rename = "uco-observable:subjectPublicKeyAlgorithm")]
    pub subject_public_key_algorithm: Option<String>,
    #[serde(rename = "uco-observable:subjectPublicKeyExponent")]
    pub subject_public_key_exponent: Option<i64>,
    #[serde(rename = "uco-observable:subjectPublicKeyModulus")]
    pub subject_public_key_modulus: Option<String>,
    #[serde(rename = "uco-observable:thumbprintHash")]
    pub thumbprint_hash: Option<Hash>,
    #[serde(rename = "uco-observable:validityNotAfter")]
    pub validity_not_after: Option<String>,
    #[serde(rename = "uco-observable:validityNotBefore")]
    pub validity_not_before: Option<String>,
    #[serde(rename = "uco-observable:version")]
    pub version: Option<String>,
    #[serde(rename = "uco-observable:x509v3extensions")]
    pub x509v3extensions: Option<X509V3ExtensionsFacet>,
}

impl X509CertificateFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/X509CertificateFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> X509CertificateFacetBuilder {
        X509CertificateFacetBuilder {
            is_self_signed: None,
            issuer: None,
            issuer_hash: None,
            serial_number: None,
            signature: None,
            signature_algorithm: None,
            subject: None,
            subject_hash: None,
            subject_public_key_algorithm: None,
            subject_public_key_exponent: None,
            subject_public_key_modulus: None,
            thumbprint_hash: None,
            validity_not_after: None,
            validity_not_before: None,
            version: None,
            x509v3extensions: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct X509CertificateFacetBuilder {
    is_self_signed: Option<bool>,
    issuer: Option<String>,
    issuer_hash: Option<Hash>,
    serial_number: Option<String>,
    signature: Option<String>,
    signature_algorithm: Option<String>,
    subject: Option<String>,
    subject_hash: Option<Hash>,
    subject_public_key_algorithm: Option<String>,
    subject_public_key_exponent: Option<i64>,
    subject_public_key_modulus: Option<String>,
    thumbprint_hash: Option<Hash>,
    validity_not_after: Option<String>,
    validity_not_before: Option<String>,
    version: Option<String>,
    x509v3extensions: Option<X509V3ExtensionsFacet>,
}

impl X509CertificateFacetBuilder {
    pub fn is_self_signed(mut self, value: bool) -> Self {
        self.is_self_signed = Some(value);
        self
    }

    pub fn issuer(mut self, value: String) -> Self {
        self.issuer = Some(value);
        self
    }

    pub fn issuer_hash(mut self, value: Hash) -> Self {
        self.issuer_hash = Some(value);
        self
    }

    pub fn serial_number(mut self, value: String) -> Self {
        self.serial_number = Some(value);
        self
    }

    pub fn signature(mut self, value: String) -> Self {
        self.signature = Some(value);
        self
    }

    pub fn signature_algorithm(mut self, value: String) -> Self {
        self.signature_algorithm = Some(value);
        self
    }

    pub fn subject(mut self, value: String) -> Self {
        self.subject = Some(value);
        self
    }

    pub fn subject_hash(mut self, value: Hash) -> Self {
        self.subject_hash = Some(value);
        self
    }

    pub fn subject_public_key_algorithm(mut self, value: String) -> Self {
        self.subject_public_key_algorithm = Some(value);
        self
    }

    pub fn subject_public_key_exponent(mut self, value: i64) -> Self {
        self.subject_public_key_exponent = Some(value);
        self
    }

    pub fn subject_public_key_modulus(mut self, value: String) -> Self {
        self.subject_public_key_modulus = Some(value);
        self
    }

    pub fn thumbprint_hash(mut self, value: Hash) -> Self {
        self.thumbprint_hash = Some(value);
        self
    }

    pub fn validity_not_after(mut self, value: String) -> Self {
        self.validity_not_after = Some(value);
        self
    }

    pub fn validity_not_before(mut self, value: String) -> Self {
        self.validity_not_before = Some(value);
        self
    }

    pub fn version(mut self, value: String) -> Self {
        self.version = Some(value);
        self
    }

    pub fn x509v3extensions(mut self, value: X509V3ExtensionsFacet) -> Self {
        self.x509v3extensions = Some(value);
        self
    }

    pub fn build(self) -> X509CertificateFacet {
        X509CertificateFacet {
            class_iri: X509CertificateFacet::CLASS_IRI,
            is_self_signed: self.is_self_signed,
            issuer: self.issuer,
            issuer_hash: self.issuer_hash,
            serial_number: self.serial_number,
            signature: self.signature,
            signature_algorithm: self.signature_algorithm,
            subject: self.subject,
            subject_hash: self.subject_hash,
            subject_public_key_algorithm: self.subject_public_key_algorithm,
            subject_public_key_exponent: self.subject_public_key_exponent,
            subject_public_key_modulus: self.subject_public_key_modulus,
            thumbprint_hash: self.thumbprint_hash,
            validity_not_after: self.validity_not_after,
            validity_not_before: self.validity_not_before,
            version: self.version,
            x509v3extensions: self.x509v3extensions,
        }
    }
}

impl CaseObject for X509CertificateFacet {
    fn class_iri() -> &'static str { X509CertificateFacet::CLASS_IRI }
    fn type_name() -> &'static str { "X509CertificateFacet" }
}

/// An X.509 v3 certificate is a public key digital identity certificate conformant to the X.509 v3 PKI (Public Key Infrastructure) standard. 
#[derive(Debug, Clone, Serialize)]
pub struct X509V3Certificate {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
}

impl X509V3Certificate {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/X509V3Certificate";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> X509V3CertificateBuilder {
        X509V3CertificateBuilder {
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct X509V3CertificateBuilder {
}

impl X509V3CertificateBuilder {
    pub fn build(self) -> X509V3Certificate {
        X509V3Certificate {
            class_iri: X509V3Certificate::CLASS_IRI,
        }
    }
}

impl CaseObject for X509V3Certificate {
    fn class_iri() -> &'static str { X509V3Certificate::CLASS_IRI }
    fn type_name() -> &'static str { "X509V3Certificate" }
}

/// An X.509 v3 certificate extensions facet is a grouping of characteristics unique to a public key digital identity certificate conformant to the X.509 v3 PKI (Public Key Infrastructure) standard.
#[derive(Debug, Clone, Serialize)]
pub struct X509V3ExtensionsFacet {
    #[serde(skip_serializing)]
    pub class_iri: &'static str,
    #[serde(rename = "uco-observable:authorityKeyIdentifier")]
    pub authority_key_identifier: Option<String>,
    #[serde(rename = "uco-observable:basicConstraints")]
    pub basic_constraints: Option<String>,
    #[serde(rename = "uco-observable:certificatePolicies")]
    pub certificate_policies: Option<String>,
    #[serde(rename = "uco-observable:crlDistributionPoints")]
    pub crl_distribution_points: Option<String>,
    #[serde(rename = "uco-observable:extendedKeyUsage")]
    pub extended_key_usage: Option<String>,
    #[serde(rename = "uco-observable:inhibitAnyPolicy")]
    pub inhibit_any_policy: Option<String>,
    #[serde(rename = "uco-observable:issuerAlternativeName")]
    pub issuer_alternative_name: Option<String>,
    #[serde(rename = "uco-observable:keyUsage")]
    pub key_usage: Option<String>,
    #[serde(rename = "uco-observable:nameConstraints")]
    pub name_constraints: Option<String>,
    #[serde(rename = "uco-observable:policyConstraints")]
    pub policy_constraints: Option<String>,
    #[serde(rename = "uco-observable:policyMappings")]
    pub policy_mappings: Option<String>,
    #[serde(rename = "uco-observable:privateKeyUsagePeriodNotAfter")]
    pub private_key_usage_period_not_after: Option<String>,
    #[serde(rename = "uco-observable:privateKeyUsagePeriodNotBefore")]
    pub private_key_usage_period_not_before: Option<String>,
    #[serde(rename = "uco-observable:subjectAlternativeName")]
    pub subject_alternative_name: Option<String>,
    #[serde(rename = "uco-observable:subjectDirectoryAttributes")]
    pub subject_directory_attributes: Option<String>,
    #[serde(rename = "uco-observable:subjectKeyIdentifier")]
    pub subject_key_identifier: Option<String>,
}

impl X509V3ExtensionsFacet {
    pub const CLASS_IRI: &'static str = "https://ontology.unifiedcyberontology.org/uco/observable/X509V3ExtensionsFacet";
    pub const NAMESPACE_PREFIX: &'static str = "uco-observable";

    pub fn builder() -> X509V3ExtensionsFacetBuilder {
        X509V3ExtensionsFacetBuilder {
            authority_key_identifier: None,
            basic_constraints: None,
            certificate_policies: None,
            crl_distribution_points: None,
            extended_key_usage: None,
            inhibit_any_policy: None,
            issuer_alternative_name: None,
            key_usage: None,
            name_constraints: None,
            policy_constraints: None,
            policy_mappings: None,
            private_key_usage_period_not_after: None,
            private_key_usage_period_not_before: None,
            subject_alternative_name: None,
            subject_directory_attributes: None,
            subject_key_identifier: None,
        }
    }
}

#[derive(Debug, Default, Clone)]
pub struct X509V3ExtensionsFacetBuilder {
    authority_key_identifier: Option<String>,
    basic_constraints: Option<String>,
    certificate_policies: Option<String>,
    crl_distribution_points: Option<String>,
    extended_key_usage: Option<String>,
    inhibit_any_policy: Option<String>,
    issuer_alternative_name: Option<String>,
    key_usage: Option<String>,
    name_constraints: Option<String>,
    policy_constraints: Option<String>,
    policy_mappings: Option<String>,
    private_key_usage_period_not_after: Option<String>,
    private_key_usage_period_not_before: Option<String>,
    subject_alternative_name: Option<String>,
    subject_directory_attributes: Option<String>,
    subject_key_identifier: Option<String>,
}

impl X509V3ExtensionsFacetBuilder {
    pub fn authority_key_identifier(mut self, value: String) -> Self {
        self.authority_key_identifier = Some(value);
        self
    }

    pub fn basic_constraints(mut self, value: String) -> Self {
        self.basic_constraints = Some(value);
        self
    }

    pub fn certificate_policies(mut self, value: String) -> Self {
        self.certificate_policies = Some(value);
        self
    }

    pub fn crl_distribution_points(mut self, value: String) -> Self {
        self.crl_distribution_points = Some(value);
        self
    }

    pub fn extended_key_usage(mut self, value: String) -> Self {
        self.extended_key_usage = Some(value);
        self
    }

    pub fn inhibit_any_policy(mut self, value: String) -> Self {
        self.inhibit_any_policy = Some(value);
        self
    }

    pub fn issuer_alternative_name(mut self, value: String) -> Self {
        self.issuer_alternative_name = Some(value);
        self
    }

    pub fn key_usage(mut self, value: String) -> Self {
        self.key_usage = Some(value);
        self
    }

    pub fn name_constraints(mut self, value: String) -> Self {
        self.name_constraints = Some(value);
        self
    }

    pub fn policy_constraints(mut self, value: String) -> Self {
        self.policy_constraints = Some(value);
        self
    }

    pub fn policy_mappings(mut self, value: String) -> Self {
        self.policy_mappings = Some(value);
        self
    }

    pub fn private_key_usage_period_not_after(mut self, value: String) -> Self {
        self.private_key_usage_period_not_after = Some(value);
        self
    }

    pub fn private_key_usage_period_not_before(mut self, value: String) -> Self {
        self.private_key_usage_period_not_before = Some(value);
        self
    }

    pub fn subject_alternative_name(mut self, value: String) -> Self {
        self.subject_alternative_name = Some(value);
        self
    }

    pub fn subject_directory_attributes(mut self, value: String) -> Self {
        self.subject_directory_attributes = Some(value);
        self
    }

    pub fn subject_key_identifier(mut self, value: String) -> Self {
        self.subject_key_identifier = Some(value);
        self
    }

    pub fn build(self) -> X509V3ExtensionsFacet {
        X509V3ExtensionsFacet {
            class_iri: X509V3ExtensionsFacet::CLASS_IRI,
            authority_key_identifier: self.authority_key_identifier,
            basic_constraints: self.basic_constraints,
            certificate_policies: self.certificate_policies,
            crl_distribution_points: self.crl_distribution_points,
            extended_key_usage: self.extended_key_usage,
            inhibit_any_policy: self.inhibit_any_policy,
            issuer_alternative_name: self.issuer_alternative_name,
            key_usage: self.key_usage,
            name_constraints: self.name_constraints,
            policy_constraints: self.policy_constraints,
            policy_mappings: self.policy_mappings,
            private_key_usage_period_not_after: self.private_key_usage_period_not_after,
            private_key_usage_period_not_before: self.private_key_usage_period_not_before,
            subject_alternative_name: self.subject_alternative_name,
            subject_directory_attributes: self.subject_directory_attributes,
            subject_key_identifier: self.subject_key_identifier,
        }
    }
}

impl CaseObject for X509V3ExtensionsFacet {
    fn class_iri() -> &'static str { X509V3ExtensionsFacet::CLASS_IRI }
    fn type_name() -> &'static str { "X509V3ExtensionsFacet" }
}
