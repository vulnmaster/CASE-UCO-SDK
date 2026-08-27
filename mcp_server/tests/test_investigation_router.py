"""Tests for general investigation-type routing (route_investigation_content)."""

from __future__ import annotations

from pathlib import Path

from investigation_router import (
    build_extension_gap_guidance,
    detect_families,
    route_investigation_content,
    _installed_extensions,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PERRY_GRAPH = (
    PROJECT_ROOT
    / "examples/pacer/wdmo_2022_cr_04065/perry-odell-wdmo-2022-militia.jsonld"
)

VIOLENT_CRIME_TEXT = (
    "Third superseding indictment charges conspiracy to murder a federal "
    "officer, attempted murder of seven FBI agents, assault with a deadly "
    "or dangerous weapon, and 924(c) use of a firearm in furtherance of a "
    "crime of violence by two militia members. Sentencing memorandum "
    "recommends consecutive life terms and restitution."
)

CRYPTO_TEXT = (
    "Money laundering conspiracy moving stolen bitcoin through a darknet "
    "market and a mixer, chain hopping between wallets, with a forfeiture "
    "money judgment against the cryptocurrency exchange accounts."
)

CAC_TEXT = (
    "NCMEC CyberTip report of online grooming of a minor victim via chat, "
    "ICAC task force executed a search warrant, CSAM located on the device."
)

INSIDER_THREAT_TEXT = (
    "Superseding indictment charges theft of trade secrets under 18 U.S.C. "
    "1832 and economic espionage under 18 U.S.C. 1831: a software engineer "
    "uploaded more than 1,000 files of proprietary information from the "
    "corporate network to a personal account while affiliating with a "
    "foreign startup, evading data loss prevention monitoring, and asked a "
    "colleague to scan his badge after his resignation was planned."
)

CHAT_EXPORT_TEXT = (
    "English translation of WeChat messages: chat participants list for "
    "group chat 48483066127@chatroom, 242 messages, voice call records, "
    "and shared files exchanged in the group."
)

ESPIONAGE_TEXT = (
    "Indictment charges willful retention and transmission of national "
    "defense information under 18 U.S.C. 793(e), the Espionage Act: an Air "
    "National Guardsman holding a TOP SECRET//SCI security clearance "
    "transcribed classified documents from a classified workstation, "
    "printed and removed classified documents from the SCIF, and posted "
    "images bearing SECRET and TOP SECRET classification markings to a "
    "social media platform, constituting unauthorized disclosure of "
    "classified information under Executive Order 13526."
)

EXPORT_CONTROL_TEXT = (
    "Indictment charges conspiracy to violate IEEPA under 50 U.S.C. 1705 "
    "and 15 C.F.R. 764.2(d), smuggling of goods under 18 U.S.C. 554, and "
    "false export information: defendants caused the export of an EAR99 "
    "dual-use wafer scribing machine from the United States to an entity "
    "designated on the Department of Commerce Entity List, without an "
    "export license from the Bureau of Industry and Security, by filing "
    "false electronic export information through the Automated Export "
    "System naming an intermediary trading company as the ultimate "
    "consignee to conceal the true end user."
)

CTI_APT_TEXT = (
    "Cisco Talos threat spotlight: the Lotus Blossom advanced persistent "
    "threat (APT) cyber espionage group deploys the Sagerunex backdoor and "
    "post-compromise hacking tools. The actor gains persistence by using "
    "reg add to install the backdoor as a service DLL under "
    "HKLM\\SYSTEM\\CurrentControlSet\\Services and configuring it to run as "
    "a Windows service, uses Impacket for lateral movement, and tunnels "
    "command and control through Dropbox, Twitter, and Zimbra webmail as C2 "
    "channels. IOCs include campaign codes, ClamAV and Snort signatures, "
    "and the mtrain/HTran port relay tool."
)

UNSEEN_TEXT = (
    "Quarterly livestock auction ledger reconciliation discrepancies at the "
    "county fairground concession stand."
)


def test_violent_crime_routes_to_legalproc() -> None:
    matches = detect_families(VIOLENT_CRIME_TEXT)
    ids = [m["family_id"] for m in matches]
    assert "violent-crime" in ids
    assert "legal-filings-docket" in ids
    violent = next(m for m in matches if m["family_id"] == "violent-crime")
    assert "legalproc" in violent["extensions"]
    assert "docs/recipes/legal-process-modeling.md" in violent["recipes"]


def test_crypto_routes_to_cryptoinv() -> None:
    matches = detect_families(CRYPTO_TEXT)
    crypto = next(m for m in matches if m["family_id"] == "financial-crime-crypto")
    assert "cryptoinv" in crypto["extensions"]


KIDNAPPING_TEXT = (
    "Second superseding indictment: the defendants kidnapped Victim A at "
    "gunpoint and held him for ransom over a $6,000 methamphetamine drug "
    "debt, a Hobbs Act robbery of his vehicle, brandishing a firearm under "
    "924(c), felon in possession of a SIG Sauer P365 pistol, and conspiracy "
    "to possess with intent to distribute 500 grams or more of a mixture "
    "containing methamphetamine, a Schedule II controlled substance under "
    "21 U.S.C. 841(a)(1) and 846."
)


def test_kidnapping_routes_to_violent_crime_with_weapons() -> None:
    matches = detect_families(KIDNAPPING_TEXT)
    ids = [m["family_id"] for m in matches]
    assert "violent-crime" in ids
    assert "drug-trafficking" in ids
    violent = next(m for m in matches if m["family_id"] == "violent-crime")
    assert "weapons" in violent["extensions"]
    assert "docs/recipes/weapons-drug-evidence.md" in violent["recipes"]


MURDER_FOR_HIRE_TEXT = (
    "One-count indictment for Use of Interstate Facility in Commission of "
    "Murder-for-Hire in violation of 18 U.S.C. 1958: the defendant offered "
    "to pay a couple at least $20,000 per killing to murder three people, "
    "confirmed in a video-recorded call that she wanted the victim killed "
    "as soon as possible, and paid $10,000 after a staged failed attempt. "
    "The jury returned a guilty verdict and the court imposed the "
    "statutory-maximum sentence of 120 months."
)


def test_murder_for_hire_routes_to_violent_crime() -> None:
    matches = detect_families(MURDER_FOR_HIRE_TEXT)
    ids = [m["family_id"] for m in matches]
    assert "violent-crime" in ids
    violent = next(m for m in matches if m["family_id"] == "violent-crime")
    assert "legalproc" in violent["extensions"]
    assert "murder for hire" in violent["matched_keywords"] or "1958" in violent["matched_keywords"]


RACKETEERING_TEXT = (
    "Second superseding indictment charges seventeen defendants with RICO "
    "conspiracy under 18 U.S.C. 1962(d): members and associates of a "
    "social engineering enterprise, a group of individuals associated in "
    "fact although not a legal entity, agreed to conduct the affairs of "
    "the enterprise through a pattern of racketeering activity including "
    "wire fraud and laundering of monetary instruments. The enterprise's "
    "division of labor included database hackers, organizers, target "
    "identifiers, callers, money launderers, and a residential burglar."
)


def test_racketeering_routes_to_rico_extension() -> None:
    matches = detect_families(RACKETEERING_TEXT)
    ids = [m["family_id"] for m in matches]
    assert "racketeering-enterprise" in ids
    rico = next(m for m in matches if m["family_id"] == "racketeering-enterprise")
    assert "rico" in rico["extensions"]
    assert "legalproc" in rico["extensions"]
    assert "docs/recipes/racketeering-enterprise.md" in rico["recipes"]
    payload = route_investigation_content(PROJECT_ROOT, content_text=RACKETEERING_TEXT)
    assert payload["ok"] is True
    assert payload["matched_families"][0]["family_id"] == "racketeering-enterprise"


def test_drug_trafficking_routes_to_drugs_extension() -> None:
    matches = detect_families(
        "DEA seized two kilograms of fentanyl and heroin; conspiracy to "
        "possess with intent to distribute a controlled substance under "
        "841(a)(1) and 846, with a drug quantity finding."
    )
    drug = next(m for m in matches if m["family_id"] == "drug-trafficking")
    assert "drugs" in drug["extensions"]
    assert "legalproc" in drug["extensions"]
    assert "weapons" in drug["extensions"]
    assert "docs/recipes/weapons-drug-evidence.md" in drug["recipes"]


def test_route_full_payload_violent_crime() -> None:
    payload = route_investigation_content(PROJECT_ROOT, content_text=VIOLENT_CRIME_TEXT)
    assert payload["ok"] is True
    assert payload["matched_families"]
    top = payload["matched_families"][0]
    assert top["family_id"] in {"violent-crime", "legal-filings-docket"}
    # legalproc manifest discovered on disk
    assert any(
        detail["name"] == "legalproc"
        for m in payload["matched_families"]
        for detail in m["extension_details"]
    )
    assert any("CASE_UCO_EXTENSIONS" in step for step in payload["recommended_workflow"])
    # Upper-profile hints resolve to human guidance
    assert any(m["upper_profile_hints"] for m in payload["matched_families"])


def test_cac_content_points_to_cac_router() -> None:
    payload = route_investigation_content(PROJECT_ROOT, content_text=CAC_TEXT)
    ids = [m["family_id"] for m in payload["matched_families"]]
    assert "cac-child-exploitation" in ids
    assert payload["next_tools"]["cac_deep_routing"] is not None
    cac = next(m for m in payload["matched_families"] if m["family_id"] == "cac-child-exploitation")
    assert "attack-technique" not in cac["extensions"]
    assert "ATT&CK is not CAC community language" in cac["notes"]
    assert "hackers and attackers" in cac["notes"]


def test_insider_threat_routes_to_corporate_internal() -> None:
    matches = detect_families(INSIDER_THREAT_TEXT)
    assert matches, "insider-threat text must match at least one family"
    top = matches[0]
    assert top["family_id"] == "corporate-internal"
    assert "legalproc" in top["extensions"]
    assert "docs/recipes/insider-threat-trade-secrets.md" in top["recipes"]


def test_chat_export_routes_to_email_messaging() -> None:
    matches = detect_families(CHAT_EXPORT_TEXT)
    ids = [m["family_id"] for m in matches]
    assert "email-messaging" in ids
    messaging = next(m for m in matches if m["family_id"] == "email-messaging")
    assert "docs/recipes/threaded-messaging.md" in messaging["recipes"]


def test_espionage_routes_to_national_security() -> None:
    matches = detect_families(ESPIONAGE_TEXT)
    assert matches, "espionage text must match at least one family"
    top = matches[0]
    assert top["family_id"] == "national-security-espionage"
    assert "legalproc" in top["extensions"]
    assert "docs/recipes/espionage-classified-disclosure.md" in top["recipes"]
    assert "uco-marking" in top["core_namespaces"]


def test_export_control_routes_to_export_control_family() -> None:
    matches = detect_families(EXPORT_CONTROL_TEXT)
    assert matches, "export control text must match at least one family"
    top = matches[0]
    assert top["family_id"] == "export-control-sanctions"
    assert "legalproc" in top["extensions"]
    assert "docs/recipes/export-control-sanctions.md" in top["recipes"]


def test_cti_apt_routes_to_cyber_threat_intelligence_family() -> None:
    matches = detect_families(CTI_APT_TEXT)
    assert matches, "CTI/APT text must match at least one family"
    top = matches[0]
    assert top["family_id"] == "cyber-threat-intelligence"
    assert "docs/recipes/cyber-threat-intelligence.md" in top["recipes"]
    # Registry/persistence data is pure-core, but MITRE ATT&CK techniques are
    # modeled with the attack-technique extension (uco-action:Technique, #666).
    assert "attack-technique" in top["extensions"]
    assert "uco-tool" in top["core_namespaces"]
    assert "Do not use this family for crimes-against-children" in top["notes"]


def test_unseen_data_returns_extension_gap_guidance() -> None:
    payload = route_investigation_content(PROJECT_ROOT, content_text=UNSEEN_TEXT)
    assert payload["matched_families"] == []
    guidance = payload["extension_gap_guidance"]
    assert any("draft_change_proposal" in step for step in guidance["workflow"])
    assert "docs/recipes/extensions.md" in guidance["recipes"]


def test_graph_file_submission_routes() -> None:
    payload = route_investigation_content(PROJECT_ROOT, source_path=str(PERRY_GRAPH))
    assert payload["ok"] is True
    ids = [m["family_id"] for m in payload["matched_families"]]
    assert "violent-crime" in ids or "legal-filings-docket" in ids


def test_installed_extensions_discovered() -> None:
    installed = _installed_extensions(PROJECT_ROOT)
    assert {"cac", "cryptoinv", "legalproc"} <= set(installed)
    assert installed["legalproc"]["namespaces"]["legalproc"] == "https://ontology.caseontology.org/case/criminal/"


def test_full_sysdiagnose_routing_guidance_is_distinct() -> None:
    payload = route_investigation_content(
        PROJECT_ROOT,
        content_text=(
            "Full sysdiagnose_2026.08.11_iPhone-OS tree with "
            "system_logs.logarchive, WiFi/, summaries/, crashes_and_spins/, "
            "Preferences/, and BatteryBDC files."
        ),
    )
    guidance = payload["apple_collect_guidance"]
    assert guidance["claimed_shape"] == "ios-sysdiagnose"
    assert guidance["recipes"][0] == "docs/recipes/ios-sysdiagnose.md"
    assert payload["next_tools"]["apple_package_classifier"] is not None


def test_standalone_foss_collect_is_not_claimed_as_sysdiagnose() -> None:
    payload = route_investigation_content(
        PROJECT_ROOT,
        content_text=(
            "FOSS iOS collection with standalone.logarchive, crash pull, "
            "live syslog, and installed apps list; this is not a sysdiagnose. "
            "The archive has no timesync."
        ),
    )
    guidance = payload["apple_collect_guidance"]
    assert guidance["claimed_shape"] == "apple-foss-logarchive"
    assert "docs/recipes/ios-sysdiagnose.md" not in guidance["recipes"]
    assert guidance["recipes"][0] == "docs/recipes/apple-unified-logs.md"
    assert "omit absolute device UTC" in guidance["timesync_guidance"]


def test_ambiguous_logarchive_routing_defers_to_local_classifier() -> None:
    payload = route_investigation_content(
        PROJECT_ROOT,
        content_text="Apple iOS standalone .logarchive collected for review.",
    )
    guidance = payload["apple_collect_guidance"]
    assert guidance["claimed_shape"] == "unconfirmed-apple-logarchive"
    assert "classify_apple_package_shape" in guidance["authoritative_next_tool"]


def test_gap_guidance_is_self_contained() -> None:
    guidance = build_extension_gap_guidance()
    joined = " ".join(guidance["workflow"])
    for tool in ("search_classes", "get_uco_profiles", "check_existing_proposals", "validate_graph"):
        assert tool in joined
