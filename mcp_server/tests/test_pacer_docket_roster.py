"""Tier T0 tests for structural PACER docket roster parsing.

The failure these guard against: a PACER defendant block contains the
"represented by" attorney block, so a string-level reading of the block
promotes defense counsel to the charged party.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from document_semantic_mapping import extract_pacer_docket_roster, extract_semantic_entities

# Synthetic docket in the layout the real sheets use.
SYNTHETIC_PACER_DOCKET_ROSTER = """
U.S. District Court
Eastern District of Testland (Testville)
CRIMINAL DOCKET FOR CASE #: 1:25-cr-00999-XYZ All Defendants
Case title: USA v. Rowan et al Date Filed: 01/02/2026
Assigned to: Judge Dana Reyes
Defendant (1)
Priya Rowan
also known as
Kestrel
also known as
Bluejay
represented by Marcus Delacroix
Law Office of Marcus Delacroix, PLLC
100 Test Street
Testville, TS 10001
555-010-1000
Email: marcus@example-counsel.test
LEAD ATTORNEY
ATTORNEY TO BE NOTICED
Designation: CJA Appointment
Nadia Okonkwo
Okonkwo Law PLLC
P.O. Box 9
Testville, TS 10002
Email: nadia@example-counsel.test
LEAD ATTORNEY
Designation: CJA Appointment
Pending Counts Disposition
Title 18, United States Code, Section 1001 - False Statements.
(1)
Defendant (2)
Aiden Vasquez
also known as
Rook
represented by Tomas Iverson
Iverson & Bright PC
200 Test Avenue
Testville, TS 10003
Email: tomas@example-counsel.test
LEAD ATTORNEY
Designation: Retained
Pending Counts Disposition
Title 18, United States Code, Section 1001 - False Statements.
(1)
Plaintiff
USA represented by Harper Quinn
Date Filed # Docket Text
01/02/2026 1 SEALED INDICTMENT as to Priya Rowan (1) count(s) 1, 2, 3, Aiden Vasquez (2) count(s) 1, 3.
"""

JURISDICTION_CAPTION = """
UNITED STATES DISTRICT COURT
EASTERN DISTRICT OF NEW YORK
Assigned to: Judge Dana Reyes
Violation One occurred within the District of New Mexico.
Violation Two occurred within the Southern District of California.
"""


def test_roster_separates_defendants_from_counsel() -> None:
    roster = extract_pacer_docket_roster(SYNTHETIC_PACER_DOCKET_ROSTER)
    defendants = roster["defendants"]

    assert [entry["name"] for entry in defendants] == ["Priya Rowan", "Aiden Vasquez"]
    assert defendants[0]["defendant_number"] == 1
    assert defendants[0]["aliases"] == ["Kestrel", "Bluejay"]
    assert defendants[0]["counsel"] == ["Marcus Delacroix", "Nadia Okonkwo"]
    assert defendants[1]["aliases"] == ["Rook"]
    assert defendants[1]["counsel"] == ["Tomas Iverson"]

    # No defendant may also be reported as counsel, and vice versa.
    assert not any(entry["name"] in roster["counsel_names"] for entry in defendants)
    assert "Marcus Delacroix" in roster["counsel_names"]


def test_roster_rejects_firm_and_address_lines_as_counsel() -> None:
    roster = extract_pacer_docket_roster(SYNTHETIC_PACER_DOCKET_ROSTER)
    for firm in (
        "Law Office of Marcus Delacroix, PLLC",
        "Okonkwo Law PLLC",
        "Iverson & Bright PC",
        "P.O. Box 9",
    ):
        assert firm not in roster["counsel_names"]


def test_roster_reads_the_docket_entry_one_count_matrix() -> None:
    matrix = extract_pacer_docket_roster(SYNTHETIC_PACER_DOCKET_ROSTER)["count_matrix"]
    assert matrix == [
        {"defendant_number": 1, "name": "Priya Rowan", "counts": [1, 2, 3]},
        {"defendant_number": 2, "name": "Aiden Vasquez", "counts": [1, 3]},
    ]


def test_roster_is_empty_for_non_docket_text() -> None:
    roster = extract_pacer_docket_roster(JURISDICTION_CAPTION)
    assert roster["defendants"] == []
    assert roster["count_matrix"] == []
    assert roster["counsel_names"] == []


def test_jurisdictions_are_not_extracted_as_people() -> None:
    entities = extract_semantic_entities(JURISDICTION_CAPTION, run_seed="jurisdiction-t0")
    people = {
        entity.label
        for entity in entities
        if entity.ontology_class == "uco-identity:Person"
    }
    for token in ("New York", "New Mexico", "Eastern District", "District Court", "United States"):
        assert not any(token in label for label in people), f"{token} extracted as Person: {people}"


# A charging instrument names the same victim across many counts, and every
# page of a PACER PDF repeats the case number and document stamp in its header.
REPEATED_MENTIONS = """
Case 1:25-cr-00999-XYZ Document 8 Filed 12/02/25 Page 1 of 4
COUNT ONE
Minor Victim 3 and Minor Victim 4 were solicited by the defendants.
Case 1:25-cr-00999-XYZ Document 8 Filed 12/02/25 Page 2 of 4
COUNT TWO
The defendants distributed images of Minor Victim 3.
Case 1:25-cr-00999-XYZ Document 8 Filed 12/02/25 Page 3 of 4
Minor Victim 3 was later identified. Minor Victim 4 resided in Testland.
Case 1:25-cr-00999-XYZ Document 8 Filed 12/02/25 Page 4 of 4
"""

ACCOUNT_PROSE = """
Discord was the primary communications platform used by the group.
Members used either Discord or another service for Discord calls.
The defendant used the Discord account "fiasco_2019" to contact the victim.
A co-conspirator was reachable at Telegram @northstar_mike_synth.
"""


def _labels(text: str, ontology_class: str, seed: str) -> list[str]:
    return [
        entity.label
        for entity in extract_semantic_entities(text, run_seed=seed)
        if entity.ontology_class == ontology_class
    ]


def test_repeated_victim_labels_resolve_to_one_node_each() -> None:
    victims = _labels(REPEATED_MENTIONS, "uco-identity:Person", "victims-t0")
    assert sorted(victims) == ["Minor Victim 3", "Minor Victim 4"]


def test_repeated_page_headers_do_not_become_separate_events() -> None:
    events = _labels(REPEATED_MENTIONS, "uco-core:Event", "headers-t0")
    assert events.count("Federal case 1:25-cr-00999-XYZ") == 1
    assert events.count("PACER filing Document 8") == 1


def test_prose_after_a_platform_name_is_not_an_account() -> None:
    accounts = _labels(ACCOUNT_PROSE, "uco-observable:ApplicationAccount", "accounts-t0")
    for noise in ("Discord was", "Discord or", "Discord calls"):
        assert noise not in accounts, f"phrase chunk extracted as account: {accounts}"


def test_real_handles_are_still_extracted() -> None:
    accounts = _labels(ACCOUNT_PROSE, "uco-observable:ApplicationAccount", "accounts-t0")
    assert "Discord fiasco_2019" in accounts
    assert "Telegram northstar_mike_synth" in accounts


def test_repeated_filing_stamps_do_not_multiply_date_events() -> None:
    events = _labels(REPEATED_MENTIONS, "uco-core:Event", "dates-t0")
    assert events.count("Date 12/02/25") == 1


def test_header_noise_does_not_crowd_out_late_entities() -> None:
    """Extraction is capped at MAX_SEMANTIC_ENTITIES nodes.

    Before deduplication, a long PACER PDF spent that budget on repeated page
    headers and dropped real entities appearing later in the document.
    """
    header = (
        "Case 1:25-cr-00999-XYZ Document 8 Filed 12/02/25 Page {page} of 200\n"
        "COUNT ONE\n"
        "The defendants acted on January 28, 2020.\n"
    )
    padded = "".join(header.format(page=page) for page in range(1, 200))
    padded += "\nMinor Victim 9 and Minor Victim 10 were identified later.\n"

    victims = {
        label
        for label in _labels(padded, "uco-identity:Person", "budget-t0")
        if label.startswith("Minor Victim")
    }
    assert victims == {"Minor Victim 9", "Minor Victim 10"}
