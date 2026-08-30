"""Route any investigation submission to recipes, extensions, and ontologies.

Hermes, Link-Look, and other MCP callers submit warrant returns, legal
filings, case files, semi-structured and fully-structuredextraction reports, existing CASE/UCO graphs,and free-text narratives covering
many investigation types — not only CAC. This module classifies the
submission into one or more investigation families and, for each, returns
the recipes to follow, the extension ontologies to enable, the core
CASE/UCO namespaces involved, and (when relevant) the CDO upper-ontology
profiles to lean on. When nothing matches — a previously unseen data type —
it returns the extension-gap workflow instead of guessing.

Guidance-only: callers build the graph; validate_graph enforces SHACL and
strict concept coverage afterward.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import semantic_retrieval
from apple_acquisition import apple_collect_guidance
from cac_content_router import (
    GENERIC_CAC_KEYWORDS,
    _normalize_text,
    assess_extraction_quality,
    detect_cac_domains,
    resolve_submission_text,
)

MIN_FAMILY_SCORE = 2

# Primary composition recipe for multi-domain / cross-ontology graphs (#66).
# Prefer this over the legacy cross-domain-extensions.md redirect stub.
COMPOSITION_RECIPE = "docs/recipes/cross-ontology-composition.md"

# CAC domain families that are specific to child exploitation. The other CAC
# router domains (federal prosecution, PACER ingestion, task force, ...) match
# generic legal/investigative text and must not imply CAC by themselves.
CAC_SPECIFIC_DOMAIN_IDS = frozenset({
    "grooming-chat", "cybertip-ncmec", "trafficking-recruitment",
    "victim-rescue-extraction", "icac-search-warrant-arrest",
    "sextortion-coercion", "hotline-intake", "csam-forensic-provenance",
    "missing-child-investigation", "production-case",
})


# A CAC routing decision additionally requires an explicit child-related
# token; the CAC router's substring keywords ("ring", "recruitment",
# "search warrant", ...) match generic criminal text on their own.
CHILD_SIGNAL_TOKENS = (
    "child", "minor", "juvenile", "underage", "csam", "cybertip", "ncmec",
    "icac", "sextortion", "grooming", "student", "teen",
)


def _cac_specific_signals(text: str) -> list[dict[str, Any]]:
    normalized = _normalize_text(text)
    child_tokens = sum(1 for token in CHILD_SIGNAL_TOKENS if token in normalized)
    generic_hit = any(kw in normalized for kw in GENERIC_CAC_KEYWORDS)
    # One incidental "child(ren)" mention in a non-CAC filing must not route
    # to CAC; require either a generic CAC phrase or multiple child tokens.
    if not generic_hit and child_tokens < 2:
        return []
    if generic_hit:
        return detect_cac_domains(text) or [{"domain_id": "cac-general", "score": 1, "recipe_file": COMPOSITION_RECIPE}]
    return [d for d in detect_cac_domains(text) if d["domain_id"] in CAC_SPECIFIC_DOMAIN_IDS]


@dataclass(frozen=True)
class InvestigationFamily:
    """One investigation-type routing entry (broader than a CAC domain)."""

    family_id: str
    title: str
    keywords: tuple[str, ...]
    recipes: tuple[str, ...]
    extensions: tuple[str, ...] = ()
    core_namespaces: tuple[str, ...] = ()
    upper_profiles: tuple[str, ...] = ()
    notes: str = ""


@dataclass
class OrderedRoutingRecommendations:
    """Typed ordered-routing payload (CQ-40)."""

    primary_composition_recipe: str | None
    supporting_domain_recipes: list[str]
    required_extensions: list[str]
    recommended_profiles: list[str]
    optional_profiles: list[str]
    not_recommended_profiles: list[str]
    validation_bundle_preview: dict[str, Any] | None
    compatibility_warnings: list[str]
    ontology_gap_workflow: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


INVESTIGATION_FAMILIES: tuple[InvestigationFamily, ...] = (
    InvestigationFamily(
        family_id="cac-child-exploitation",
        title="Crimes Against Children (CAC)",
        keywords=(
            "csam", "child exploitation", "child sexual abuse", "grooming",
            "cybertip", "ncmec", "icac", "sextortion", "minor victim",
            "trafficking a minor", "child pornography", "enticement",
            "internet crimes against children", "child victim",
        ),
        recipes=("docs/recipes/cac-pacer-document-ingestion.md",),
        extensions=("cac",),
        core_namespaces=("case-investigation", "uco-observable", "uco-action", "uco-identity", "uco-victim"),
        upper_profiles=("gUFO",),
        notes=(
            "Call route_cac_content for per-domain CAC recipes, modeling "
            "checklists, and CAC validation guidance — it covers 17 CAC "
            "domain families in depth. ATT&CK is not CAC community "
            "language. A CAC offender targets children and other "
            "vulnerable people; ATT&CK models hackers and attackers. "
            "Do not emit ATT&CK techniques or call the subject a threat "
            "actor unless the source describes that rare overlap."
        ),
    ),
    InvestigationFamily(
        family_id="violent-crime",
        title="Violent Crime and Domestic Terrorism",
        keywords=(
            "murder", "attempted murder", "assault", "homicide", "kidnapping",
            "attempted to kill", "shooting", "shot at", "militia",
            "domestic terrorism", "crime of violence", "deadly or dangerous weapon",
            "bodily injury", "body armor", "ammunition", "carjacking",
            "victim", "armed", "hostage", "threat to injure", "arson",
            "federal officer", "federal crime of terrorism", "924(c)",
            "ransom", "abduct", "held for ransom", "hobbs act", "robbery",
            "brandish", "felon in possession", "1201(a)", "at gunpoint",
            "murder-for-hire", "murder for hire", "1958",
            "solicitation to commit murder", "hitman", "hired to kill",
            "killed as soon as possible", "pay to kill",
        ),
        recipes=(
            "docs/recipes/legal-process-modeling.md",
            "docs/recipes/weapons-drug-evidence.md",
            "docs/recipes/cac-pacer-document-ingestion.md",
            "docs/recipes/event.md",
            "docs/recipes/forensic-lifecycle.md",
        ),
        extensions=("legalproc", "weapons"),
        core_namespaces=("case-investigation", "uco-action", "uco-identity", "uco-observable", "uco-victim", "uco-role"),
        upper_profiles=("PROV-O", "OWL-Time", "GeoSPARQL", "gUFO"),
        notes=(
            "Model charges with legalproc:CriminalCharge and record "
            "conspiracy/attempt/derivative counts via offenseForm + "
            "objectOffense. Firearms and ammunition use the weapons "
            "extension (weap:Handgun, weap:Rifle, weap:Ammunition with "
            "make/model/caliber/serialNumber; CCO Artifact Ontology and "
            "gUFO grounding via bridge files) instead of bare UcoObject "
            "descriptions. Vehicles and other artifacts without extension "
            "classes stay uco-core:UcoObject dual-typed "
            "gufo:FunctionalComplex. Seized/charged drug quantities use "
            "the drugs extension (drug:ControlledSubstance, ChEBI IRI via "
            "drug:substance, gufo:Quantity grounding). uco-action:performer "
            "is max-1: primary actor as performer, co-actors linked with "
            "Participated_In relationships. Digital overt acts (social "
            "posts, texts, ransom calls as uco-observable:Call) are UCO "
            "observables. Exemplars: examples/pacer/wdmo_2022_cr_04065/ "
            "(militia) and examples/pacer/ndnd_2025_cr_00005/ (kidnapping "
            "over a drug debt, first weapons+drugs exemplar)."
        ),
    ),
    InvestigationFamily(
        family_id="drug-trafficking",
        title="Drug Trafficking and Controlled Substances",
        keywords=(
            "methamphetamine", "fentanyl", "cocaine", "heroin", "narcotics",
            "controlled substance", "drug trafficking", "drug conspiracy",
            "possess with intent to distribute", "841(a)(1)", "841(b)(1)",
            "846", "drug debt", "drug quantity", "schedule i", "schedule ii",
            "kilogram", "grams of a mixture", "dea", "drug distribution",
            "drug paraphernalia", "overdose",
        ),
        recipes=(
            "docs/recipes/weapons-drug-evidence.md",
            "docs/recipes/legal-process-modeling.md",
            "docs/recipes/cac-pacer-document-ingestion.md",
        ),
        extensions=("drugs", "legalproc", "weapons"),
        core_namespaces=("case-investigation", "uco-action", "uco-identity", "uco-observable", "uco-location"),
        upper_profiles=("gUFO",),
        notes=(
            "Model each seized or charged quantity as a "
            "drug:ControlledSubstance (drugs extension): chemical identity "
            "by ChEBI IRI reference via drug:substance (methamphetamine "
            "CHEBI_6809, fentanyl CHEBI_119915, cocaine CHEBI_27958, "
            "heroin CHEBI_27808), csaSchedule per 21 U.S.C. § 812, "
            "mass/massUnit with the verbatim charging language in "
            "quantityDescription, and purityBasis 'mixture' vs 'actual' "
            "(USSG § 2D1.1). The portion is linked to, not typed by, the "
            "chemical class; the gUFO bridge grounds it as gufo:Quantity. "
            "Firearms charged under 924(c)/922(g) alongside drug counts "
            "use the weapons extension. Charges, pleas, and sentences use "
            "legalproc. Exemplar: examples/pacer/ndnd_2025_cr_00005/."
        ),
    ),
    InvestigationFamily(
        family_id="financial-crime-crypto",
        title="Financial Crime, Cryptocurrency, and Money Laundering",
        keywords=(
            "cryptocurrency", "bitcoin", "btc", "ethereum", "blockchain",
            "wallet", "money laundering", "laundering", "mixer", "darknet market",
            "wire fraud", "bank fraud", "peel chain", "chain hopping",
            "virtual asset", "exchange account", "fiat", "structuring",
            "forfeiture money judgment", "unlicensed money transmitting",
            "elder fraud", "scheme to defraud", "false personation",
            "impersonation", "money mule", "courier", "runner",
            "green dot", "gift card", "prepaid card", "tech support scam",
            "grandparent scam", "romance scam", "call center",
            "spoofed", "caller id",
        ),
        recipes=(
            "docs/recipes/fraud-crypto-laundering.md",
            "docs/recipes/elder-fraud-impersonation.md",
            "docs/recipes/legal-process-modeling.md",
        ),
        extensions=("cryptoinv", "legalproc"),
        core_namespaces=("case-investigation", "uco-observable", "uco-action", "uco-identity"),
        upper_profiles=("PROV-O",),
        notes=(
            "Typed crypto observables (addresses, transactions, wallets, "
            "holdings) come from the cryptoinv extension tracking UCO #675. "
            "Exemplar: examples/pacer/doj_crypto_2023_239/. For "
            "government-impersonation / money-courier elder fraud (no "
            "crypto layer), follow elder-fraud-impersonation.md; exemplar: "
            "examples/pacer/edla_2022_cr_00115/."
        ),
    ),
    InvestigationFamily(
        family_id="racketeering-enterprise",
        title="Racketeering (RICO) and Criminal Enterprise",
        keywords=(
            "racketeering", "rico", "1962(d)", "1962(c)", "1961(1)",
            "criminal enterprise", "association-in-fact", "association in fact",
            "pattern of racketeering", "predicate act", "predicate acts",
            "racketeering activity", "organized crime", "criminal organization",
            "enterprise role", "division of labor", "crime family",
            "syndicate", "criminal crew", "street gang", "gang enterprise",
            "social engineering enterprise", "members and associates",
            "conduct the affairs of the enterprise",
        ),
        recipes=(
            "docs/recipes/racketeering-enterprise.md",
            "docs/recipes/legal-process-modeling.md",
            "docs/recipes/fraud-crypto-laundering.md",
            "docs/recipes/cac-pacer-document-ingestion.md",
        ),
        extensions=("rico", "legalproc"),
        core_namespaces=("case-investigation", "uco-action", "uco-identity", "uco-role", "uco-observable"),
        upper_profiles=("PROV-O", "OWL-Time", "gUFO"),
        notes=(
            "Model the charged enterprise as rico:RacketeeringEnterprise "
            "(subclass of uco-identity:Organization) with enterpriseType "
            "'association-in-fact' or 'legal-entity' per 18 U.S.C. "
            "§ 1961(4); membership as Member_Of relationships (only where "
            "a document places the person in the enterprise). The charged "
            "division of labor becomes rico:EnterpriseRole nodes "
            "(roleFunction: organizer, database-hacker, target-identifier, "
            "caller, money-launderer, residential-burglar, ...) linked "
            "with Has_Role (person→role) and Role_Within (role→"
            "enterprise). Put the § 1961(1) predicate categories on every "
            "RICO CriminalCharge node as repeatable rico:predicateStatute "
            "values. Charges/pleas/sentences use legalproc with PACER "
            "count suffixes (1/1s/1ss) verbatim in countLabel; add "
            "cryptoinv (launderingTechnique, VirtualAssetServiceProvider, "
            "crypto address facets) when the enterprise deals in virtual "
            "assets. Never equate coconspirator initials with named "
            "defendants. Exemplar: examples/pacer/ddc_2024_cr_00417/ "
            "(U.S. v. Lam et al., the SE Enterprise, first rico exemplar)."
        ),
    ),
    InvestigationFamily(
        family_id="legal-filings-docket",
        title="Court Filings, Dockets, and Legal Process",
        keywords=(
            "pacer", "docket", "indictment", "superseding indictment",
            "information", "plea agreement", "sentencing memorandum",
            "judgment", "grand jury", "arraignment", "supervised release",
            "restitution", "forfeiture", "count", "u.s.c.", "statement of offense",
            "presentence investigation", "guilty plea", "verdict", "trial brief",
            "notice of appeal", "criminal complaint", "warrant return",
        ),
        recipes=(
            "docs/recipes/legal-process-modeling.md",
            "docs/recipes/cac-pacer-document-ingestion.md",
            "docs/recipes/technique-evidence-outcome.md",
            "docs/recipes/legal-discovery-disclosure.md",
        ),
        extensions=("legalproc",),
        core_namespaces=("case-investigation", "uco-action", "uco-identity", "uco-observable"),
        upper_profiles=("PROV-O", "OWL-Time"),
        notes=(
            "Process PDFs with process_document_file first (OCR fallback for "
            "scanned filings), keep SHA-256 provenance on each source "
            "document, and never fabricate date precision the filing does "
            "not state."
        ),
    ),
    InvestigationFamily(
        family_id="network-intrusion",
        title="Network Intrusion and Cyber Attack",
        keywords=(
            "pcap", "packet capture", "intrusion", "malware", "ransomware",
            "phishing", "spear phishing", "command and control", "c2 server",
            "ip address", "exfiltration", "lateral movement", "botnet",
            "ddos", "vulnerability", "exploit", "backdoor", "compromise",
        ),
        recipes=(
            "docs/recipes/network-investigation.md",
            "docs/recipes/network-artifacts.md",
            "docs/recipes/spear-phishing.md",
        ),
        core_namespaces=("uco-observable", "uco-action", "case-investigation"),
        upper_profiles=("PROV-O", "OWL-Time"),
    ),
    InvestigationFamily(
        family_id="device-mobile-forensics",
        title="Device and Mobile Forensics",
        keywords=(
            "mobile extraction", "cellebrite", "ufed", "graykey", "axiom",
            "imei", "sim card", "sms", "call log", "device extraction",
            "physical extraction", "logical extraction", "chip-off",
            "smartphone", "android", "iphone", "app data",
            "sysdiagnose", "logarchive", "unified log", "unified logs",
            "tracev3", "ufade", "pymobiledevice3", "ileapp",
        ),
        recipes=(
            "docs/recipes/starter-mobile-extraction.md",
            "docs/recipes/mobile-device.md",
            "docs/recipes/mobile-device-sim.md",
            "docs/recipes/sms-and-contacts.md",
            "docs/recipes/ios-sysdiagnose.md",
            "docs/recipes/apple-unified-logs.md",
            "docs/recipes/solve-it-investigation-planning.md",
            "docs/recipes/technique-evidence-outcome.md",
        ),
        extensions=("solveit",),
        core_namespaces=("uco-observable", "uco-action", "uco-tool"),
        upper_profiles=("PROV-O",),
    ),
    InvestigationFamily(
        family_id="email-messaging",
        title="Email and Messaging Evidence",
        keywords=(
            "email export", "mailbox", "pst", "mbox", "eml", "email header",
            "thread", "chat log", "message thread", "instant message",
            "whatsapp", "telegram", "signal", "imessage", "conversation export",
            "wechat", "chatroom", "group chat", "chat participants",
            "translation of chat", "voice call",
        ),
        recipes=(
            "docs/recipes/starter-email-export.md",
            "docs/recipes/email-messaging.md",
            "docs/recipes/threaded-messaging.md",
        ),
        core_namespaces=("uco-observable", "uco-identity"),
        upper_profiles=("FOAF",),
    ),
    InvestigationFamily(
        family_id="filesystem-media",
        title="Filesystem, Disk, and Media Forensics",
        keywords=(
            "disk image", "filesystem report", "file listing", "hash list",
            "hash set", "e01", "dd image", "partition", "usn journal",
            "carving", "file recovery", "deleted file", "unallocated",
            "volume shadow", "ntfs", "exfat",
        ),
        recipes=(
            "docs/recipes/starter-filesystem-report.md",
            "docs/recipes/file-system.md",
            "docs/recipes/file-recovery.md",
            "docs/recipes/partitions.md",
            "docs/recipes/solve-it-investigation-planning.md",
        ),
        extensions=("solveit",),
        core_namespaces=("uco-observable", "uco-types", "uco-tool"),
        upper_profiles=("PROV-O",),
    ),
    InvestigationFamily(
        family_id="forensic-process-qa",
        title="Forensic Process, Technique Selection, and Quality Assurance",
        keywords=(
            "solve-it", "solveit", "error mitigation", "error mitigation analysis",
            "technique selection", "tool testing", "tool validation",
            "dual-tool verification", "quality assurance", "lab accreditation",
            "examination methodology", "methodology challenge", "daubert",
            "error rate", "astm e3016", "weakness assessment",
            "acquisition plan", "imaging procedure", "write blocker",
            "hash verification", "standard operating procedure", "sop",
            "peer review of examination", "competency test", "proficiency test",
            "hash match", "photodna", "usedtechnique", "legal outcome",
            "effectiveness",
        ),
        recipes=(
            "docs/recipes/solve-it-investigation-planning.md",
            "docs/recipes/technique-evidence-outcome.md",
            "docs/recipes/forensic-lifecycle.md",
            "docs/recipes/forensic-tool.md",
            "docs/recipes/chain-of-custody.md",
        ),
        extensions=("solveit",),
        core_namespaces=("case-investigation", "uco-action", "uco-tool", "uco-analysis"),
        upper_profiles=("PROV-O",),
        notes=(
            "Document forensic method with the pinned SOLVE-IT knowledge "
            "base (ontology/solveit/): record each step as a "
            "solveit-core:SolveitInvestigativeAction with usedTechnique "
            "(DFT-*) and appliedMitigation (DFM-*), and rate residual risk "
            "with solveit-wa:WeaknessEvaluation (ASTM E3016-18 categories). "
            "Use plan_solveit_workflow(text) to go from an investigation "
            "goal to candidate techniques with per-technique weakness/"
            "mitigation checklists, and search_solveit / "
            "get_solveit_details for the catalog. Exemplar: "
            "examples/solveit/."
        ),
    ),
    InvestigationFamily(
        family_id="civil-ediscovery",
        title="Civil Litigation and E-Discovery",
        keywords=(
            "legal hold", "e-discovery", "ediscovery", "discovery request",
            "civil action", "class action", "settlement", "civil judgment",
            "interrogatories", "deposition", "litigation hold", "custodian",
            "regulatory enforcement", "consent decree",
        ),
        recipes=(
            "docs/recipes/change-proposal.md",
            "docs/recipes/extensions.md",
            "docs/recipes/recipe-authoring.md",
        ),
        core_namespaces=("case-investigation", "uco-observable", "uco-action"),
        upper_profiles=("PROV-O",),
        notes=(
            "Civil process stub concepts (CivilAction, LegalHold, "
            "DiscoveryRequest, Settlement) are proposed but not yet adopted "
            "— see https://github.com/casework/CASE/issues/193. Model with "
            "core CASE/UCO plus a local extension implementing the #193 "
            "stubs (pattern: extensions/legalproc/)."
        ),
    ),
    InvestigationFamily(
        family_id="corporate-internal",
        title="Corporate Insider Threat and Internal Investigations",
        keywords=(
            "internal investigation", "insider threat", "policy violation",
            "hr investigation", "disciplinary", "code of conduct",
            "whistleblower", "corporate mandate", "exit interview",
            "data loss prevention", "acceptable use", "termination",
            "trade secret", "economic espionage", "theft of trade secrets",
            "1832", "1831", "proprietary information", "confidential information",
            "exfiltrat", "personal account", "employment agreement",
            "badge", "resignation", "resigned", "talent program",
            "foreign instrumentality", "competitor", "startup",
            "non-compete", "source code theft",
        ),
        recipes=(
            "docs/recipes/insider-threat-trade-secrets.md",
            "docs/recipes/legal-process-modeling.md",
            "docs/recipes/change-proposal.md",
            "docs/recipes/extensions.md",
        ),
        extensions=("legalproc",),
        core_namespaces=("case-investigation", "uco-observable", "uco-action", "uco-identity"),
        upper_profiles=("ORG", "PROV-O", "gUFO"),
        notes=(
            "For prosecuted trade-secret theft / economic espionage, follow "
            "insider-threat-trade-secrets.md (exemplar: "
            "examples/pacer/ndca_2024_cr_00141/). The insider is an "
            "*authorized* user — model exfiltration with uco-action:Action "
            "plus per-category trade secret observables, not intrusion "
            "patterns. Corporate process stub concepts "
            "(CorporateInvestigationMandate, PolicyViolation, "
            "DisciplinaryOutcome, Referral) are proposed but not yet "
            "adopted — see https://github.com/casework/CASE/issues/194."
        ),
    ),
    InvestigationFamily(
        family_id="national-security-espionage",
        title="National Security, Espionage Act, and Classified Information",
        keywords=(
            "espionage", "espionage act", "793", "794", "national defense information",
            "classified information", "classified document", "top secret",
            "security clearance", "scif", "sensitive compartmented information",
            "//sci", "ts//sci", "noforn", "fvey", "unauthorized disclosure",
            "executive order 13526", "executive order 12958", "declassif",
            "original classification authority", "jwics", "siprnet",
            "controlled unclassified information", "classification level",
            "classification marking", "need to know", "indoctrination",
            "leak of classified", "clearance holder", "intelligence community",
        ),
        recipes=(
            "docs/recipes/espionage-classified-disclosure.md",
            "docs/recipes/legal-process-modeling.md",
            "docs/recipes/insider-threat-trade-secrets.md",
        ),
        extensions=("legalproc",),
        core_namespaces=("case-investigation", "uco-observable", "uco-action", "uco-identity", "uco-marking"),
        upper_profiles=("PROV-O", "gUFO"),
        notes=(
            "For Espionage Act (18 U.S.C. §§ 793/794) and classified-"
            "information cases, follow espionage-classified-disclosure.md "
            "(exemplar: examples/pacer/dma_2023_cr_10159/). USG "
            "classification banners on charged NDI are uco-marking "
            "MarkingDefinition + StatementMarking nodes attached via "
            "uco-core:objectMarking — preserve banners verbatim as the "
            "charging instrument attests them, and never promote "
            "malformed or defendant-quoted banner strings (e.g. a "
            "contradictory NOFORN + FVEY combination) to markings. "
            "Distinguish from corporate-internal: § 1831/1832 protects "
            "corporate trade secrets; § 793/794 protects government "
            "national defense information."
        ),
    ),
    InvestigationFamily(
        family_id="export-control-sanctions",
        title="Export Control and Sanctions Evasion",
        keywords=(
            "export control", "ieepa", "1705", "export administration regulations",
            "15 c.f.r", "entity list", "commerce control list", "eccn", "ear99",
            "export license", "bureau of industry and security", "denied party",
            "specially designated national", "sdn list", "ofac", "sanctions evasion",
            "embargo", "itar", "arms export control act", "2778", "munitions list",
            "shipper's export declaration", "electronic export information",
            "automated export system", "ultimate consignee", "end user", "end-user",
            "freight forwarder", "transshipment", "re-export", "reexport",
            "smuggling of goods", "554", "false export information",
            "dual use", "dual-use", "export control reform act",
        ),
        recipes=(
            "docs/recipes/export-control-sanctions.md",
            "docs/recipes/legal-process-modeling.md",
            "docs/recipes/cac-pacer-document-ingestion.md",
        ),
        extensions=("legalproc",),
        core_namespaces=("case-investigation", "uco-observable", "uco-action", "uco-identity", "uco-location"),
        upper_profiles=("PROV-O", "gUFO"),
        notes=(
            "For IEEPA/EAR, smuggling (18 U.S.C. § 554), false export "
            "information (13 U.S.C. § 305), ITAR/AECA, and OFAC sanctions "
            "cases, follow export-control-sanctions.md (exemplar: "
            "examples/pacer/ndca_2020_cr_00446/). Entity List/SDN "
            "designations are dated regulatory Actions gating what conduct "
            "was unlawful when. The controlled item is a physical good "
            "(uco-core:UcoObject + gufo:FunctionalComplex, ECCN/EAR99 in "
            "the description — not a uco-marking data marking); the "
            "EEI/AES filings, waybills, contracts, and emails about it "
            "are the cyber observables. Model the papered-consignee vs. "
            "true-end-user concealment chain in graph structure, and use "
            "per-defendant charge nodes for shared counts. Distinguish "
            "from national-security-espionage (classified information) "
            "and corporate-internal (stolen trade secrets): here the "
            "goods were lawfully bought and unlawfully exported."
        ),
    ),
    InvestigationFamily(
        family_id="cyber-threat-intelligence",
        title="Cyber Threat Intelligence and APT Reporting",
        keywords=(
            "apt", "advanced persistent threat", "threat actor", "threat group",
            "cyber espionage", "espionage group", "nation-state", "nation state",
            "sagerunex", "backdoor", "implant", "malware family", "malware variant",
            "remote access tool", "rat", "loader", "dll injection", "vmprotect",
            "command and control", "c2", "c2 tunnel", "beacon", "exfiltration",
            "living off the land", "lateral movement", "impacket", "wmi",
            "persistence", "service dll", "servicedll", "registry persistence",
            "reg add", "run key", "scheduled task", "cookie stealer",
            "credential theft", "proxy tool", "port relay", "htran",
            "victimology", "campaign", "threat spotlight", "ttp", "ttps",
            "tactics techniques and procedures", "mitre att&ck", "att&ck",
            "technique", "indicator of compromise", "ioc", "iocs", "yara",
            "clamav", "snort", "talos", "mandiant", "threat intelligence",
            "dropbox c2", "twitter c2", "cloud c2", "third-party cloud",
        ),
        recipes=(
            "docs/recipes/cyber-threat-intelligence.md",
            "docs/recipes/network-investigation.md",
            "docs/recipes/analysis.md",
        ),
        core_namespaces=(
            "case-investigation", "uco-observable", "uco-action",
            "uco-tool", "uco-identity", "uco-location",
        ),
        extensions=("attack-technique",),
        upper_profiles=("PROV-O", "OWL-Time"),
        notes=(
            "For open-source CTI / APT threat reports (Talos, Mandiant, "
            "vendor blogs) analyzing a threat actor, its malware families, "
            "and TTPs, follow cyber-threat-intelligence.md (exemplar: "
            "examples/cti/lotus_blossom_2025/). This is intelligence about "
            "an adversary, not acquired host/network evidence: the report "
            "itself is an ObservableObject, in-report graphics are "
            "RasterPicture observables captured by hash with a description "
            "of what each depicts (they carry IOCs/config detail absent "
            "from the prose), and the threat actor is a uco-identity:"
            "Organization (UCO has no ThreatActor class) whose behaviors "
            "are uco-action:Action nodes. Malware families/tools are "
            "uco-tool:MaliciousTool; samples/variants are File observables "
            "with hashes and existence intervals. Registry persistence is "
            "fully covered by core UCO — WindowsRegistryKey + "
            "WindowsRegistryKeyFacet with embedded WindowsRegistryValue "
            "(name/data/dataType via RegistryDatatypeVocab: reg_expand_sz, "
            "reg_dword) plus WindowsService (startType service_auto_start "
            "from Start=2); no change proposal is needed for registry data. "
            "MITRE ATT&CK techniques use the uco-action:Technique metaclass "
            "(ucoProject/UCO PR #676, UCO 1.5.0): a technique is an owl:Class "
            "that is a subclass of uco-action:Action and carries "
            "uco-action:techniqueID, and a behavior Action that exhibits it is "
            "rdf:typed with that technique class (punning) — not a plain "
            "instance node and not a Uses_Technique relationship. The "
            "attack-technique extension forward-implements the metaclass, the "
            "uco-core:UcoType anchor, and a partial ATT&CK catalog; validate "
            "with extensions=['attack-technique:full'] (RDFS inference). "
            "Enrich from the MITRE group/software pages (e.g. Lotus Blossom "
            "G0030, Sagerunex S1156) even when the report prose omits IDs. "
            "Contrast with network-intrusion (single incident with acquired "
            "pcap/host evidence) and spear-phishing (delivery-chain narrative). "
            "Do not use this family for crimes-against-children investigations. "
            "ATT&CK is attacker/hacker tradecraft, not the language for a CAC "
            "offender who targets children or other vulnerable people."
        ),
    ),
)

UPPER_PROFILE_HINTS = {
    "PROV-O": "provenance chains (prov:wasDerivedFrom, prov:used) — UCO action/provenance alignment",
    "OWL-Time": "temporal intervals and precision-honest periods (time:Interval, time:hasBeginning)",
    "GeoSPARQL": "geospatial features and geometries for locations, routes, and jurisdictions",
    "gUFO": "foundational typing (events, roles, relators) used across the CAC Ontology",
    "FOAF": "social-network and account-holder structures (foaf:knows, foaf:account)",
    "ORG": "organizational structure (org:Organization, org:memberOf, org:reportsTo)",
    "BFO": "Basic Formal Ontology alignment for formal upper-level typing",
    "PROF": "validation-profile metadata (prof:Profile) — intent and resource descriptors, not SHACL results",
}

# Display names used on InvestigationFamily.upper_profiles → validation_bundle IDs.
# Built from PROFILE_REGISTRY (+ UCO_PROFILES labels); not a hard-coded parallel map (CQ-39).
def _build_profile_display_to_id() -> dict[str, str]:
    from validation_bundle import PROFILE_REGISTRY

    mapping: dict[str, str] = {}
    for pid, meta in PROFILE_REGISTRY.items():
        canonical = meta.get("alias_of", pid)
        mapping[pid] = canonical
        mapping[pid.upper()] = canonical
        mapping[pid.replace("-", "_")] = canonical
        # Common display tokens used in family hints.
        if pid == "prov-o":
            mapping["PROV-O"] = canonical
            mapping["PROV"] = canonical
        elif pid == "time":
            mapping["OWL-Time"] = canonical
            mapping["OWL_TIME"] = canonical
        elif pid == "geosparql":
            mapping["GeoSPARQL"] = canonical
        elif pid == "gufo":
            mapping["gUFO"] = canonical
            mapping["GUFO"] = canonical
        elif pid == "bfo":
            mapping["BFO"] = canonical
        elif pid == "foaf":
            mapping["FOAF"] = canonical
        elif pid == "org":
            mapping["ORG"] = canonical
        elif pid == "prof":
            mapping["PROF"] = canonical
        elif pid == "owl-time":
            mapping["OWL-Time"] = canonical
    try:
        from domain_index import UCO_PROFILES

        for profile in UCO_PROFILES:
            pid = profile["id"]
            if pid not in PROFILE_REGISTRY:
                continue
            canonical = PROFILE_REGISTRY[pid].get("alias_of", pid)
            mapping[profile.get("name", "")] = canonical
            full = profile.get("full_name") or ""
            if full:
                mapping[full] = canonical
                # Parenthetical short name, e.g. "… (gUFO)" / "… (BFO 2020)"
                if "(" in full and ")" in full:
                    inner = full.split("(", 1)[1].split(")", 1)[0].strip()
                    if inner:
                        mapping[inner] = canonical
                        mapping[inner.split()[0]] = canonical
    except Exception:  # noqa: BLE001 — discovery catalog optional at import time
        pass
    return {k: v for k, v in mapping.items() if k}


PROFILE_DISPLAY_TO_ID: dict[str, str] = _build_profile_display_to_id()

# Extension → profile policy from docs/recipes/cross-ontology-composition.md.
EXTENSION_PROFILE_POLICY: dict[str, dict[str, tuple[str, ...]]] = {
    "cac": {
        "recommended": ("gufo", "prov-o", "time", "foaf", "org"),
        "optional": ("geosparql", "prof"),
        "not_recommended": ("bfo",),
    },
    "aeo": {
        "recommended": ("prov-o", "time", "foaf"),
        "optional": ("gufo", "org", "geosparql", "prof"),
        "not_recommended": (),
    },
    "solveit": {
        "recommended": ("prov-o", "gufo"),
        "optional": ("time", "foaf", "org", "prof"),
        "not_recommended": (),
    },
    "legalproc": {
        "recommended": ("prov-o", "org", "gufo"),
        "optional": ("time", "foaf", "prof"),
        "not_recommended": (),
    },
    "rico": {
        "recommended": ("prov-o", "org", "gufo"),
        "optional": ("time", "foaf", "prof"),
        "not_recommended": (),
    },
    "cryptoinv": {
        "recommended": ("prov-o", "time", "geosparql"),
        "optional": ("foaf", "org", "gufo", "prof"),
        "not_recommended": (),
    },
    "weapons": {
        "recommended": ("prov-o", "time"),
        "optional": ("geosparql", "foaf", "gufo", "prof"),
        "not_recommended": (),
    },
    "drugs": {
        "recommended": ("prov-o", "time"),
        "optional": ("geosparql", "foaf", "gufo", "prof"),
        "not_recommended": (),
    },
}

_CORE_FORENSIC_PROFILES = {
    "recommended": ("prov-o", "time", "geosparql", "foaf"),
    "optional": ("org", "gufo", "prof"),
    "not_recommended": (),
}


def _installed_extensions(
    project_root: Path,
    integrity_failures: list[dict[str, str]] | None = None,
) -> dict[str, dict[str, Any]]:
    """Discover extension manifests bundled with the SDK.

    Only *operational* extensions are advertised (knowledge_lifecycle):
    candidate and deprecated extensions stay invisible to routing until
    promoted, although explicit loading by name still works for the
    investigation that is authoring them. Malformed manifests and invalid
    lifecycle statuses are excluded fail-closed; pass ``integrity_failures``
    to collect a typed record of each exclusion (issue #55).
    """

    from knowledge_lifecycle import extension_status, is_routable

    import extension_paths

    found: dict[str, dict[str, Any]] = {}
    for ext_dir in extension_paths.iter_extension_dirs(project_root):
        manifest_path = ext_dir / "manifest.json"
        ext_dir_name = ext_dir.name
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            if integrity_failures is not None:
                integrity_failures.append({
                    "extension": ext_dir_name,
                    "error": "extension_manifest_malformed",
                })
            continue
        status = extension_status(manifest)
        if status == "invalid" and integrity_failures is not None:
            integrity_failures.append({
                "extension": ext_dir_name,
                "error": "extension_status_invalid",
            })
        if not is_routable(manifest):
            continue
        name = manifest.get("name") or ext_dir_name
        found[name] = {
            "name": name,
            "display_name": manifest.get("display_name", name),
            "version": manifest.get("version"),
            "status": status,
            "namespaces": manifest.get("namespaces", {}),
            "path": str(manifest_path.parent.relative_to(project_root)),
        }
    return found


def keyword_in_text(normalized: str, keyword: str) -> bool:
    """Substring match, but short tokens need token boundaries.

    Otherwise ``ttp`` hits every ``https://`` IRI when a Layer-1 graph is
    routed, and ``c2`` / ``846`` / ``554`` collide with statute fragments
    and hex hashes.
    """

    needle = keyword.casefold()
    haystack = normalized.casefold()
    if len(needle) <= 4 or needle[0].isdigit():
        return re.search(rf"(?<![a-z0-9]){re.escape(needle)}(?![a-z0-9])", haystack) is not None
    return needle in haystack


def score_family(text: str, family: InvestigationFamily) -> tuple[int, list[str]]:
    normalized = _normalize_text(text)
    hits = [kw for kw in family.keywords if keyword_in_text(normalized, kw)]
    return len(hits), hits


def _family_document_text(family: InvestigationFamily) -> str:
    """Catalog text a family is semantically retrieved against."""

    return " ".join([family.title, " ".join(family.keywords), family.notes])


def _family_match_payload(
    family: InvestigationFamily,
    keyword_score: int,
    keyword_hits: list[str],
    semantic: float,
    semantic_evidence: list[str],
    stages: list[str],
) -> dict[str, Any]:
    confidence = semantic_retrieval.combined_confidence(keyword_score, semantic)
    return {
        "family_id": family.family_id,
        "title": family.title,
        "score": keyword_score,
        "matched_keywords": keyword_hits[:12],
        "match_stages": stages,
        "scoring": {
            "keyword_score": keyword_score,
            "semantic_score": round(semantic, 3),
            "confidence": confidence,
        },
        "semantic_evidence": semantic_evidence,
        "recipes": list(family.recipes),
        "extensions": list(family.extensions),
        "core_namespaces": list(family.core_namespaces),
        "upper_profiles": list(family.upper_profiles),
        "notes": family.notes,
    }


def detect_families_hybrid(text: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Two-stage hybrid routing: deterministic keywords plus offline
    lexical-semantic retrieval (semantic_retrieval module).

    Returns ``(matches, deterministic_baseline)``. The baseline records what
    the keyword stage alone matched so every result remains auditable
    against the pre-hybrid behavior. Families matched only semantically
    need ``semantic_score >= SEMANTIC_MATCH_THRESHOLD``.
    """

    matches: list[dict[str, Any]] = []
    baseline: list[dict[str, Any]] = []
    for family in INVESTIGATION_FAMILIES:
        keyword_score, keyword_hits = score_family(text, family)
        semantic, evidence = semantic_retrieval.semantic_score(
            text, _family_document_text(family)
        )
        keyword_matched = keyword_score >= MIN_FAMILY_SCORE
        semantic_matched = semantic >= semantic_retrieval.SEMANTIC_MATCH_THRESHOLD
        if keyword_matched:
            baseline.append({
                "family_id": family.family_id,
                "score": keyword_score,
                "matched_keywords": keyword_hits[:12],
            })
        if not keyword_matched and not semantic_matched:
            continue
        stages = []
        if keyword_matched:
            stages.append("keyword")
        if semantic_matched:
            stages.append("semantic")
        matches.append(
            _family_match_payload(
                family, keyword_score, keyword_hits, semantic, evidence, stages
            )
        )
    matches.sort(
        key=lambda item: (-item["scoring"]["confidence"], -item["score"], item["family_id"])
    )
    baseline.sort(key=lambda item: (-item["score"], item["family_id"]))
    return matches, baseline


def detect_families(text: str) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for family in INVESTIGATION_FAMILIES:
        score, hits = score_family(text, family)
        if score >= MIN_FAMILY_SCORE:
            matches.append({
                "family_id": family.family_id,
                "title": family.title,
                "score": score,
                "matched_keywords": hits[:12],
                "recipes": list(family.recipes),
                "extensions": list(family.extensions),
                "core_namespaces": list(family.core_namespaces),
                "upper_profiles": list(family.upper_profiles),
                "notes": family.notes,
            })
    matches.sort(key=lambda item: (-item["score"], item["family_id"]))
    return matches


def build_extension_gap_guidance() -> dict[str, Any]:
    """Workflow for previously unseen data types (no family or class match)."""

    return {
        "summary": (
            "This submission does not match a known investigation family. "
            "Do NOT invent terms — strict concept coverage will reject any "
            "class or property not declared in CASE/UCO, a bundled "
            "extension, or a profiled upper ontology."
        ),
        "workflow": [
            "1. Search for existing coverage: search_classes(keyword) and "
            + "find_classes_for_domain(task) across scope='all' (core + extensions).",
            "2. Check upper ontologies: get_uco_profiles(query) — terms from "
            + "profiled ontologies (BFO, gUFO, PROV-O, OWL-Time, GeoSPARQL, "
            + "FOAF, ORG, PROF) pass strict validation directly.",
            "3. Model what fits with core CASE/UCO: most evidence reduces to "
            + "ObservableObject+Facets, Actions, Identities, Roles, and "
            + "Relationships even in novel domains.",
            "4. For genuinely missing concepts: check_existing_proposals(concept) "
            + "to find prior UCO/CASE/CAC issues, then draft_change_proposal(...) "
            + "to file the gap upstream.",
            "5. Unblock immediately with a local extension ontology "
            + "(docs/recipes/extensions.md): OWL + SHACL files subclassing "
            + "UCO/CASE classes, a manifest.json, and dcterms:source links to "
            + "the filed proposals. Pattern to copy: extensions/legalproc/.",
            "6. Validate with validate_graph(graph_path, extensions=[...], "
            + "profiles=[...]) until Conforms: True with zero undeclared concepts.",
            "7. Once the graph validates, capture the pattern as a new "
            + "recipe — or fold it into the nearest existing recipe — per "
            + "docs/recipes/recipe-authoring.md, and register/refresh the "
            + "recipe indexes so the next agent is routed instead of "
            + "rediscovering. This is how the catalog grows with the "
            + "investigator.",
        ],
        "recipes": [
            "docs/recipes/extensions.md",
            "docs/recipes/change-proposal.md",
            COMPOSITION_RECIPE,
            "docs/recipes/recipe-authoring.md",
        ],
    }


def _profile_ids_from_display(names: list[str] | tuple[str, ...]) -> list[str]:
    """Resolve family profile hints through PROFILE_REGISTRY (CQ-39)."""
    from validation_bundle import PROFILE_REGISTRY, _normalize_profile_id

    ids: list[str] = []
    seen: set[str] = set()
    for name in names:
        raw = PROFILE_DISPLAY_TO_ID.get(name, name.lower().replace("_", "-"))
        try:
            if raw in PROFILE_REGISTRY:
                pid = _normalize_profile_id(raw)
            elif name in PROFILE_REGISTRY:
                pid = _normalize_profile_id(name)
            else:
                pid = raw
        except Exception:  # noqa: BLE001 — keep token for fail-closed preview
            pid = raw
        if pid not in seen:
            seen.add(pid)
            ids.append(pid)
    return ids


def build_ordered_recommendations(
    matches: list[dict[str, Any]],
    installed: dict[str, dict[str, Any]],
    *,
    project_root: Path | None = None,
) -> dict[str, Any]:
    """Ordered composition guidance for multi-domain / cross-ontology routing (#66).

    Builds a typed :class:`OrderedRoutingRecommendations` then returns its
    dict form for JSON/MCP payload compatibility (CQ-40).
    """

    return _build_ordered_recommendations_model(
        matches, installed, project_root=project_root
    ).to_dict()


def _build_ordered_recommendations_model(
    matches: list[dict[str, Any]],
    installed: dict[str, dict[str, Any]],
    *,
    project_root: Path | None = None,
) -> OrderedRoutingRecommendations:
    """Typed builder used by tests and :func:`build_ordered_recommendations`."""

    gap = build_extension_gap_guidance()
    if not matches:
        return OrderedRoutingRecommendations(
            primary_composition_recipe=None,
            supporting_domain_recipes=[],
            required_extensions=[],
            recommended_profiles=[],
            optional_profiles=[],
            not_recommended_profiles=[],
            validation_bundle_preview=None,
            compatibility_warnings=[
                "No investigation family matched — follow ontology_gap_workflow "
                "before inventing terms."
            ],
            ontology_gap_workflow=gap,
        )

    required_extensions = sorted({
        ext for m in matches for ext in m.get("extensions", [])
    })
    supporting: list[str] = []
    seen_recipes: set[str] = set()
    for m in matches:
        for recipe in m.get("recipes", []):
            if recipe == COMPOSITION_RECIPE or recipe in seen_recipes:
                continue
            seen_recipes.add(recipe)
            supporting.append(recipe)

    multi_domain = len(matches) > 1
    family_profiles = [
        p for m in matches for p in m.get("upper_profiles", [])
    ]
    needs_composition = (
        multi_domain
        or bool(family_profiles)
        or len(required_extensions) > 1
    )
    primary = COMPOSITION_RECIPE if needs_composition else (
        supporting[0] if supporting else COMPOSITION_RECIPE
    )
    if primary in supporting:
        supporting = [r for r in supporting if r != primary]

    recommended: list[str] = []
    optional: list[str] = []
    not_recommended: list[str] = []
    seen_rec: set[str] = set()
    seen_opt: set[str] = set()
    seen_not: set[str] = set()

    def _add(target: list[str], seen: set[str], pid: str) -> None:
        if pid not in seen:
            seen.add(pid)
            target.append(pid)

    for pid in _profile_ids_from_display(family_profiles):
        _add(recommended, seen_rec, pid)

    policies = [
        EXTENSION_PROFILE_POLICY[ext]
        for ext in required_extensions
        if ext in EXTENSION_PROFILE_POLICY
    ]
    if not policies and not family_profiles:
        policies = [_CORE_FORENSIC_PROFILES]

    for policy in policies:
        for pid in policy.get("recommended", ()):
            _add(recommended, seen_rec, pid)
        for pid in policy.get("optional", ()):
            _add(optional, seen_opt, pid)
        for pid in policy.get("not_recommended", ()):
            _add(not_recommended, seen_not, pid)

    optional = [
        p for p in optional
        if p not in seen_rec and p not in seen_not
    ]

    warnings: list[str] = []
    if multi_domain:
        titles = ", ".join(m["title"] for m in matches)
        warnings.append(
            f"Multiple families matched ({titles}): build ONE investigation "
            f"graph composing every matched family's recipes — see {COMPOSITION_RECIPE}."
        )
    if "cac" in required_extensions and "bfo" in recommended:
        recommended = [p for p in recommended if p != "bfo"]
        _add(not_recommended, seen_not, "bfo")
        warnings.append(
            "CAC is aligned with gUFO; BFO is not recommended on the same graph."
        )
    if "bfo" in recommended and "gufo" in recommended:
        recommended = [p for p in recommended if p != "bfo"]
        _add(not_recommended, seen_not, "bfo")
        warnings.append(
            "BFO and gUFO are mutually exclusive foundational profiles — "
            "select one (gUFO preferred when CAC or gUFO family hints are present)."
        )
    missing_ext = [e for e in required_extensions if e not in installed]
    if missing_ext:
        warnings.append(
            "Required extensions not found as installed operational packages: "
            + ", ".join(missing_ext)
        )

    preview: dict[str, Any] | None = None
    if missing_ext:
        # CQ-39: never silently drop missing extensions from the preview.
        preview = {
            "ok": False,
            "error": "required_extensions_missing",
            "missing_extensions": missing_ext,
            "requested_extensions": required_extensions,
            "requested_profiles": recommended,
            "unavailable": True,
        }
        warnings.append(
            "validation_bundle_preview unavailable: required extensions missing "
            f"({', '.join(missing_ext)}); install/promote them before validating."
        )
    else:
        try:
            from validation_bundle import resolve_validation_bundle

            root = project_root or Path(__file__).resolve().parents[1]
            bundle = resolve_validation_bundle(
                extensions=required_extensions or None,
                profiles=recommended or None,
                project_root=root,
            )
            preview = {
                "ok": True,
                "extensions": list(bundle.extensions),
                "profiles": list(bundle.profiles),
                "inference": bundle.inference,
                "compatibility_notes": list(bundle.compatibility_notes),
                "fingerprint": bundle.fingerprint,
                "resource_count": len(bundle.resources),
                "resources": [
                    {
                        "role": r.role,
                        "path": r.path,
                        "profile_id": r.profile_id,
                        "extension": r.extension,
                    }
                    for r in bundle.resources
                ],
            }
            warnings.extend(bundle.compatibility_notes)
        except Exception as exc:  # noqa: BLE001 — preview must never break routing
            code = getattr(exc, "code", type(exc).__name__)
            warnings.append(f"validation_bundle_preview unavailable ({code}): {exc}")
            preview = {
                "ok": False,
                "error": str(exc),
                "requested_extensions": required_extensions,
                "requested_profiles": recommended,
                "unavailable": True,
            }

    return OrderedRoutingRecommendations(
        primary_composition_recipe=primary,
        supporting_domain_recipes=supporting,
        required_extensions=required_extensions,
        recommended_profiles=recommended,
        optional_profiles=optional,
        not_recommended_profiles=not_recommended,
        validation_bundle_preview=preview,
        compatibility_warnings=warnings,
        ontology_gap_workflow=None,
    )


def build_general_workflow(matches: list[dict[str, Any]], installed: dict[str, dict[str, Any]]) -> list[str]:
    steps: list[str] = []
    extensions_needed = sorted({ext for m in matches for ext in m["extensions"] if ext in installed})
    missing_ext = sorted({ext for m in matches for ext in m["extensions"] if ext not in installed})
    if extensions_needed:
        steps.append(
            "Enable extensions: set CASE_UCO_EXTENSIONS="
            + ",".join(extensions_needed)
            + " (server) and pass extensions="
            + json.dumps(extensions_needed)
            + " to validate_graph."
        )
    if missing_ext:
        steps.append(
            "Required extensions are not installed as operational packages: "
            + ", ".join(missing_ext)
            + ". Promote/install them before relying on validation_bundle_preview."
        )
    if len(matches) > 1:
        titles = ", ".join(m["title"] for m in matches)
        steps.append(
            f"Multiple families matched ({titles}): this is ONE "
            "investigation spanning several domains, not several "
            "investigations. Build a single graph, compose the recipes from "
            "every matched family on it, and enable the union of their "
            f"extensions — see {COMPOSITION_RECIPE}. Do "
            "not split the case per family or model only the top-scoring "
            "one. Prefer ordered_recommendations for the primary composition "
            "recipe, supporting domain recipes, profiles, and validation bundle preview."
        )
    steps.extend([
        "Process binary source files with process_document_file (keeps "
        + "SHA-256 provenance; OCR fallback for scanned pages); keep one "
        + "investigation graph per case, partitioned only at natural forensic "
        + "boundaries.",
        "Model observable evidence first (documents, messages, devices, "
        + "accounts, transactions), then investigative actions with "
        + "performers and authorizations, then domain interpretation "
        + "(charges, events, roles) — never collapse evidence and "
        + "interpretation into one node.",
        "Follow each matched recipe; use guide_mapping(evidence_source) for "
        + "per-source field mapping, get_recipes(scenario) for ranked recipe "
        + "matches across the whole catalog (60+ recipes — family routing "
        + "surfaces anchors, not the full list), and "
        + "get_recipes(..., include_content=True) for full recipe text.",
        "The family recipes cover the domain interpretation layer; the "
        + "underlying evidence still uses the per-artifact recipes (devices, "
        + "files, messages, call logs, locations, accounts, EXIF, databases) "
        + "— query get_recipes for each evidence type you actually hold.",
        "Validate with validate_graph(..., extensions=[...], profiles=[...]) "
        + "— SHACL plus strict concept coverage. If undeclared concepts are "
        + "reported, follow the ontology-gap workflow instead of renaming "
        + "terms to force a pass.",
        "Close the self-improvement loop (docs/recipes/recipe-authoring.md): "
        + "if you worked out a pattern no recipe covers, write and register a "
        + "new recipe; if a recipe you followed was wrong, incomplete, or "
        + "missed by routing, improve that recipe (or its index keywords) in "
        + "place and re-validate its snippets — the catalog is how this "
        + "deployment accumulates modeling judgment for non-technical "
        + "investigators while every published pattern stays verifiable "
        + "against the public ontology specifications.",
    ])
    return steps


def route_investigation_content(
    project_root: Path,
    content_text: str | None = None,
    source_path: str | None = None,
    max_families: int = 4,
) -> dict[str, Any]:
    """Classify a submission and route it to recipes/extensions/ontologies."""

    text, input_type, input_metadata = resolve_submission_text(
        content_text=content_text,
        source_path=source_path,
        project_root=project_root,
    )

    extraction_quality = assess_extraction_quality(text)
    matches, deterministic_baseline = detect_families_hybrid(text)
    matches = matches[: max(1, max_families)]
    integrity_failures: list[dict[str, str]] = []
    installed = _installed_extensions(project_root, integrity_failures)

    cac_domains = _cac_specific_signals(text)
    cac_detected = bool(cac_domains) or bool(input_metadata.get("graph_has_cac_signals"))
    if cac_detected and not any(m["family_id"] == "cac-child-exploitation" for m in matches):
        cac_score = max((d["score"] for d in cac_domains), default=1)
        matches.append({
            "family_id": "cac-child-exploitation",
            "title": "Crimes Against Children (CAC)",
            "score": cac_score,
            "matched_keywords": [d["domain_id"] for d in cac_domains][:12],
            "match_stages": ["cac-signals"],
            "scoring": {
                "keyword_score": cac_score,
                "semantic_score": 0.0,
                # Child-safety signals route deliberately even when weak;
                # the floor keeps CAC detection out of the abstention band.
                "confidence": max(
                    semantic_retrieval.combined_confidence(cac_score, 0.0),
                    semantic_retrieval.ABSTAIN_CONFIDENCE + 0.05,
                ),
            },
            "semantic_evidence": [],
            "recipes": [d["recipe_file"] for d in cac_domains][:4],
            "extensions": ["cac"],
            "core_namespaces": ["case-investigation", "uco-observable", "uco-action"],
            "upper_profiles": ["gUFO"],
            "notes": "Call route_cac_content for the full CAC domain routing and modeling checklists.",
        })
        matches.sort(
            key=lambda item: (
                -item["scoring"]["confidence"],
                -item["score"],
                item["family_id"],
            )
        )

    # Calibrated abstention: below the abstain threshold the router returns
    # gap guidance instead of a weak guess (candidates stay visible).
    top_confidence = max(
        (m["scoring"]["confidence"] for m in matches), default=0.0
    )
    confidence_level = semantic_retrieval.confidence_level(top_confidence)
    abstained_candidates: list[dict[str, Any]] = []
    if confidence_level == "abstain" and matches:
        abstained_candidates = [
            {
                "family_id": m["family_id"],
                "scoring": m["scoring"],
                "semantic_evidence": m.get("semantic_evidence", []),
            }
            for m in matches
        ]
        matches = []

    # Attach extension availability details.
    for match in matches:
        match["extension_details"] = [
            installed[ext] for ext in match["extensions"] if ext in installed
        ]
        match["upper_profile_hints"] = {
            profile: UPPER_PROFILE_HINTS[profile]
            for profile in match["upper_profiles"]
            if profile in UPPER_PROFILE_HINTS
        }

    apple_guidance = apple_collect_guidance(text)
    payload: dict[str, Any] = {
        "ok": True,
        "input_type": input_type,
        # Submitted content is evidence, not instructions (see SECURITY.md).
        "content_trust": "untrusted-source-content",
        "matched_families": matches,
        # The keyword stage alone, for auditability of the hybrid pipeline.
        "deterministic_baseline": deterministic_baseline,
        "routing_confidence": {
            "confidence": top_confidence,
            "level": confidence_level,
            "thresholds": {
                "abstain_below": semantic_retrieval.ABSTAIN_CONFIDENCE,
                "high_at_or_above": semantic_retrieval.HIGH_CONFIDENCE,
            },
        },
        "installed_extensions": sorted(installed),
        "next_tools": {
            "cac_deep_routing": "route_cac_content(content_text=...)" if cac_detected else None,
            "recipe_discovery": "get_recipes(scenario, include_content=True) — ranked matches across the full recipe catalog",
            "class_discovery": "search_classes(query, scope='all'); find_classes_for_domain(task)",
            "upper_ontologies": "get_uco_profiles(query)",
            "per_source_mapping": "guide_mapping(evidence_source)",
            "validation": "validate_graph(graph_path, extensions=[...])",
            "apple_package_classifier": (
                "classify_apple_package_shape(package_root, profile='auto')"
                if apple_guidance else None
            ),
            "apple_package_builder": (
                "build_acquisition_package_graph(..., extensions=['solveit'])"
                if apple_guidance else None
            ),
        },
        **input_metadata,
    }
    if apple_guidance:
        payload["apple_collect_guidance"] = apple_guidance
    if integrity_failures:
        payload["extension_integrity_failures"] = integrity_failures
    if extraction_quality.get("noisy_extraction"):
        payload["extraction_quality"] = extraction_quality

    if matches:
        payload["recommended_workflow"] = build_general_workflow(matches, installed)
        payload["ordered_recommendations"] = build_ordered_recommendations(
            matches, installed, project_root=project_root
        )
        if confidence_level == "low":
            gap = build_extension_gap_guidance()
            payload["extension_gap_guidance"] = gap
            payload["ordered_recommendations"]["ontology_gap_workflow"] = gap
            payload["message"] = (
                "Weak family match — treat the routing below as a hint and "
                "confirm coverage with search_classes before modeling; the "
                "extension-gap workflow is attached in case this is a new "
                "data type."
            )
    else:
        payload["matched_families"] = []
        if abstained_candidates:
            payload["abstained_candidates"] = abstained_candidates
        gap = build_extension_gap_guidance()
        payload["extension_gap_guidance"] = gap
        payload["ordered_recommendations"] = build_ordered_recommendations(
            [], installed, project_root=project_root
        )
        payload["message"] = (
            "No known investigation family matched. This looks like a "
            "previously unseen data type — follow ontology_gap_workflow / "
            "extension_gap_guidance to confirm coverage, file change "
            "proposals, and (if needed) build a local extension ontology "
            "before modeling."
        )
    return payload
