"""Deterministic CASE/UCO semantic mapping over extracted document text.

The document processor's extraction stage produces canonical text; this
module maps high-confidence spans to verified ontology classes with
text-position anchors for the Spec026 extraction bundle. Mapping is
pattern-based (no LLM): emails, URLs, phones, dates, money, locations,
organizations, persons described in law-enforcement narratives, and a
bounded narrative Event when charge/arrest language is present.

Tier T0 synthetic fixtures only in committed tests; real officer documents
belong in local T1/T2 verification per Link-Look test-data handling.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from typing import Any

from document_models import ExtractedRecord

MAX_SEMANTIC_ENTITIES = 96

EMAIL_RE = re.compile(
    r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"
)
PHONE_RE = re.compile(
    r"(?<!\d)(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}(?!\d)"
)
URL_RE = re.compile(r"https?://[^\s<>\"']+|www\.[A-Za-z0-9.\-/]+")
MONEY_RE = re.compile(r"\$\s?\d{1,6}(?:,\d{3})*(?:\.\d{2})?")
DATE_RE = re.compile(
    r"\b(?:"
    r"\d{1,2}/\d{1,2}/\d{2,4}|"
    r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+\d{1,2},?\s+\d{4}|"
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}"
    r")\b",
    re.IGNORECASE,
)
HEADLINE_SUBJECT_RE = re.compile(
    r"\b(\d{1,3})-Year-Old\s+([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)?)\s+"
    r"(Man|Woman|male|female)\b",
    re.IGNORECASE,
)
CHARGE_NARRATIVE_RE = re.compile(
    r"\b(?:charged with|arrested|taken into custody|sexual solicitation|"
    r"child (?:sex|pornography|exploitation)|investigation into)\b",
    re.IGNORECASE,
)
ORGANIZATION_RE = re.compile(
    r"\b(?:"
    r"Maryland State Police(?:\s+[A-Za-z\s]+(?:Unit|Force|Task Force))?|"
    r"Anne Arundel County Police Department|"
    r"Anchorage Police Department|"
    r"Federal Bureau of Investigation|"
    r"FBI(?:\s+Portland(?:\s+Resident Agency)?)?|"
    r"Internet Crimes Against Children(?:\s+Task Force)?|"
    r"ICAC(?:\s+Task Force)?|"
    r"United States Attorney(?:'s Office)?|"
    r"United States District Court|"
    r"United States Bureau of Prisons|"
    r"United States Secret Service|"
    r"U\.S\.\s+Secret Service|"
    r"Naval Criminal Investigative Service|"
    r"National Center for Missing(?:\s+and|&)\s+Exploited Children|"
    r"Homeland Security Investigations|"
    r"Immigration and Customs Enforcement|"
    r"Drug Enforcement Administration|"
    r"Bureau of Alcohol, Tobacco, Firearms(?:\s+and Explosives)?|"
    r"Child Exploitation and Obscenity Section|"
    r"Coinbase|Pacific Rim OTC|"
    r"NCMEC|NCIS|CEOS"
    r")\b",
    re.IGNORECASE,
)
PACER_CASE_NUMBER_RE = re.compile(
    r"\b(?:Case\s+)?(\d:\d{2}-[a-z]{2}-\d{3,5}(?:-[A-Z0-9]{1,8}){0,3})\b",
    re.IGNORECASE,
)
PACER_ECF_DOCUMENT_RE = re.compile(
    r"\bCase\s+\d:\d{2}-[a-z]{2}-\d{3,5}(?:-[A-Z0-9]{1,8}){0,3}\s+"
    r"Document\s+(\d+)\s+Filed\s+(\d{1,2}/\d{1,2}/\d{2,4})\b",
    re.IGNORECASE,
)
FEDERAL_STATUTE_RE = re.compile(
    r"\b((?:15|18|21|22|26|31|50)\s+U\.S\.C\.?\s+§§?\s*"
    r"\d+[A-Z]?(?:\([a-z0-9,\s]+\))*(?:\s*(?:and|,)\s*\([a-z0-9,\s]+\))*)"
    r"|"
    r"\b(15\s+C\.F\.R\.?\s+§?\s*[\d.]+(?:\([a-z0-9]+\))*)",
    re.IGNORECASE,
)
USC_SECTION_PROSE_RE = re.compile(
    r"\bTitle\s+(\d{1,2}),?\s+United States Code,?\s+Sections?\s+"
    r"(\d+[A-Z]?(?:\([a-z0-9]+\))*)",
    re.IGNORECASE,
)
US_V_CAPTION_RE = re.compile(
    r"UNITED\s+STATES\s+OF\s+AMERICA[\s\S]{0,120}?\bv\.?\s+"
    r"([A-Z][A-Z][A-Z .'\-]{1,80}?)(?:\s*,|\s+a/?k/?a|\s+Defendant|\s+and\b)",
)
FORENSIC_TOOL_RE = re.compile(
    r"\b("
    r"Cellebrite(?:\s+UFED)?|"
    r"UFED|"
    r"Magnet(?:\s+AXIOM)?|"
    r"AXIOM|"
    r"AccessData\s+FTK|"
    r"FTK(?:\s+Imager)?|"
    r"Autopsy|"
    r"EnCase|"
    r"GrayKey|"
    r"X-Ways(?:\s+Forensics)?|"
    r"Oxygen\s+Forensic|"
    r"MSAB\s+XRY"
    r")\b",
    re.IGNORECASE,
)
PHOTO_DNA_MATCH_RE = re.compile(
    r"PhotoDNA.{0,48}(?:match|hash)|(?:match|hash).{0,48}PhotoDNA",
    re.IGNORECASE,
)
FORENSIC_IMAGE_METHOD_RE = re.compile(
    r"\b(?:forensic(?:ally)?(?:\s+\w+){0,4}\s+imag(?:e|ed|ing)|bit[- ]stream(?:\s+copy)?)\b",
    re.IGNORECASE,
)
MOBILE_EXTRACTION_METHOD_RE = re.compile(
    r"\b(?:logical\s+extraction|physical\s+extraction|"
    r"extracted?\s+(?:the\s+)?(?:file\s+system|device\s+data))\b",
    re.IGNORECASE,
)
IMPOSED_CUSTODY_RE = re.compile(
    r"(?:imprisonment|committed to the custody|sentenced to(?: a term of)?)"
    r"(?:.{0,80}?(?:Bureau of Prisons|BOP))?.{0,40}?"
    r"(\d{1,3}\s+(?:month|months|year|years)|life(?: imprisonment)?)",
    re.IGNORECASE,
)
SUPERVISED_RELEASE_TERM_RE = re.compile(
    r"supervised release.{0,48}?(\d{1,3}\s+(?:month|months|year|years))",
    re.IGNORECASE,
)
GUILTY_PLEA_RE = re.compile(
    r"\b(?:pleads? guilty|guilty plea|entered a plea of guilty|plea of guilty)\b",
    re.IGNORECASE,
)
PLATFORM_ACCOUNT_RE = re.compile(
    r"\b(?P<platform>Snapchat|Instagram|Kik|Discord|Telegram|WhatsApp|Facebook|"
    r"Twitter|TikTok|OnlyFans|Grindr)\s+"
    r"(?P<marker>account(?:\s+name)?|username|handle|user)?\s*"
    r"(?P<quote>[\"'\u201c])?"
    # A handle may contain interior periods but must not end on one, otherwise
    # sentence-final punctuation is absorbed into the account identifier.
    r"(?P<handle>@?[A-Za-z0-9_][A-Za-z0-9_.]{0,62}[A-Za-z0-9_])",
    re.IGNORECASE,
)

# Prose that follows a platform name is not an account handle. Without this
# guard, narrative sentences such as "Discord was a communications platform"
# and "either Discord or another video conferencing platform" each yield an
# ApplicationAccount named after the next word.
ACCOUNT_HANDLE_STOPWORDS = frozenset(
    {
        "a", "an", "and", "app", "application", "are", "as", "at", "be", "been",
        "being", "but", "by", "call", "calls", "channel", "channels", "chat",
        "chats", "communication", "communications", "contained", "conversation",
        "conversations", "data", "direct", "for", "from", "group", "groups",
        "had", "has", "have", "in", "is", "it", "its", "message", "messages",
        "messaging", "on", "or", "platform", "platforms", "profile", "record",
        "records", "server", "servers", "so", "that", "the", "their", "then",
        "there", "they", "this", "to", "user", "users", "video", "voice", "was",
        "were", "when", "where", "which", "with",
    }
)


def _is_plausible_account_handle(handle: str, marked: bool) -> bool:
    """Whether a token after a platform name is really an account identifier.

    ``marked`` means the source signalled an account explicitly: an ``@``
    prefix, surrounding quotes, or a preceding word like "account" or
    "username". Unmarked tokens must look like a handle rather than an
    English word, otherwise ordinary prose becomes account observables.
    """

    bare = handle.lstrip("@")
    if not bare or bare.casefold() in ACCOUNT_HANDLE_STOPWORDS:
        return False
    if marked:
        return True
    # An unmarked handle must carry handle-like shape: a digit, underscore, or
    # internal period. "Discord calls" fails; "Discord jsmith_01" passes.
    return any(char.isdigit() or char in "_." for char in bare)
INDICTMENT_COUNT_RE = re.compile(
    r"\bCOUNT\s+(\d{1,2})\b",
    re.IGNORECASE,
)
FEDERAL_DEFENDANT_AKA_RE = re.compile(
    r"\b([A-Z][A-Z]+(?: [A-Z][A-Z]+)+)\s*,\s*a/?k/?a\s+"
    r"[\u201c\"']([^\u201d\"']+?)[\"\u201d'],?",
)
MINOR_VICTIM_RE = re.compile(
    r"\bMinor\s+Victim\s+(\d{1,2})\b",
    re.IGNORECASE,
)
SNAPCHAT_ACCOUNT_RE = re.compile(
    r"Snapchat account\s+[\u201c\"']([A-Za-z0-9_]+)[\"\u201d']",
    re.IGNORECASE,
)
SNAPCHAT_USERNAME_RE = re.compile(
    r"Snapchat\s+(?:account,?\s+)?([a-z][a-z0-9_]{2,64})\b",
    re.IGNORECASE,
)
FEDERAL_DISTRICT_RE = re.compile(
    r"\b(?:FOR THE )?DISTRICT OF ([A-Z][A-Za-z .]+?)(?:\n|\)|,|\.)",
)
# Warrant/legal prose uses many "in the …" phrases that are not locations.
LOCATION_RE = re.compile(
    r"\bresidence in\s+([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)?)\b|"
    r"\b([A-Z][a-z]+)\s+(?:Man|Woman)\b",
    re.IGNORECASE,
)
LOCATION_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "the",
        "this",
        "that",
        "these",
        "those",
        "matter",
        "affidavit",
        "summary",
        "devices",
        "device",
        "premises",
        "subject",
        "asset",
        "assets",
        "district",
        "united",
        "states",
        "seized",
        "electronic",
        "virtual",
        "currency",
        "money",
        "laundering",
        "coinbase",
        "withdrawals",
        "usdt",
        "investigation",
        "execution",
        "authorization",
        "service",
        "return",
        "court",
        "data",
        "evidence",
        "records",
        "platform",
        "administration",
        "compliance",
    }
)
US_STREET_ADDRESS_RE = re.compile(
    r"(?:\*\*)?"
    r"(\d{1,6}\s+[A-Za-z0-9][A-Za-z0-9.\- ]*?"
    r"(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Court|Ct|Way|Place|Pl)\.?)"
    r"\s*,\s*"
    r"([A-Za-z .\-]+?)\s*,\s*"
    r"([A-Za-z .\-]+?)\s+"
    r"(\d{5}(?:-\d{4})?)"
    r"(?:\*\*)?",
    re.IGNORECASE,
)
BOLD_PERSON_NAME_RE = re.compile(
    r"\*\*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+(?:\s*\([^)]+\))?)\*\*"
)
PERSON_AKA_RE = re.compile(
    r"\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\s*,\s*aka\s+[\"']([^\"']+)[\"']",
    re.IGNORECASE,
)
PERSON_OF_RE = re.compile(
    r"\bof\s+\*?\*?([A-Z][a-z]+)\s+([A-Z][a-z]+)\*?\*?\s*(?:\(|,|\.)"
)
ROLE_TABLE_PERSON_RE = re.compile(
    r"\|\s*(?:Applying Agent|Victim|Groomer|Analyst|Mule(?:\s*/\s*cash-out)?|"
    r"Account Holder|Exchange User|Registered User)\s*\|\s*"
    r"(?:Special Agent\s+)?([A-Z][a-z]+)\s+([A-Z][a-z]+)"
    r"(?:\s*,\s*aka\s+[\"']([^\"']+)[\"'])?",
    re.IGNORECASE,
)
MARKDOWN_TABLE_ROW_RE = re.compile(
    r"^\|\s*([^|\n]+?)\s*\|\s*([^|\n]+?)\s*\|\s*$",
    re.MULTILINE,
)
MARKDOWN_TABLE_SEPARATOR_RE = re.compile(r"^\|\s*[-: |]+\|\s*[-: |]+\|\s*$")
TABLE_HEADER_LABELS = frozenset({"role", "field", "label", "column", "name", "attribute"})
CHAT_SPEAKER_LINE_RE = re.compile(
    r"^([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*)\s+\(@([A-Za-z0-9_]{3,64})\)\s*:",
    re.MULTILINE,
)
ACCOUNT_HOLDER_RE = re.compile(
    r"\b(?:Account(?:\s+holder|\s+name)|Customer(?:\s+name)?|Registered user)\s*:\s*"
    r"([A-Z][a-z]+)\s+([A-Z][a-z]+)\b",
    re.IGNORECASE,
)
TELEGRAM_HANDLE_RE = re.compile(r"(?<![A-Za-z0-9])@([A-Za-z0-9_]{3,64})\b")
ETH_WALLET_RE = re.compile(r"\b(0x[a-fA-F0-9]{40})\b")
TRON_WALLET_RE = re.compile(r"\b(T[1-9A-HJ-NP-Za-km-z]{33})\b")
DOMAIN_HOST_RE = re.compile(
    r"\b([A-Za-z0-9](?:[A-Za-z0-9\-]{0,62}[A-Za-z0-9])\.example\.invalid)\b",
    re.IGNORECASE,
)
PERSON_NAME_STOPWORDS = frozenset(
    {
        "electronic",
        "devices",
        "device",
        "account",
        "accounts",
        "records",
        "virtual",
        "currency",
        "search",
        "seizure",
        "warrant",
        "magistrate",
        "judge",
        "special",
        "agent",
        "subject",
        "asset",
        "assets",
        "premises",
        "investment",
        "fraud",
        "scheme",
        "platform",
        "infrastructure",
        "synthetic",
        "training",
        "data",
        "only",
        "not",
        "evidence",
        "capital",
        "vault",
        "northstar",
        "agency",
        "portland",
        "coach",
        "analyst",
        "matter",
        "seizure",
        "criminal",
        "procedure",
        "rules",
        "federal",
        "grand",
        "jury",
        "foreperson",
        "plaintiff",
        "defendant",
        # Jurisdiction, court and venue tokens. PACER captions put these in the
        # same title-case shape as personal names, so an unguarded NER pass
        # emits "New York" and "Eastern District" as uco-identity:Person.
        "york",
        "mexico",
        "jersey",
        "hampshire",
        "carolina",
        "dakota",
        "virginia",
        "island",
        "columbia",
        "brooklyn",
        "manhattan",
        "eastern",
        "western",
        "northern",
        "southern",
        "middle",
        "district",
        "districts",
        "circuit",
        "division",
        "court",
        "courthouse",
        "states",
        "america",
        "united",
    }
)

# PACER criminal docket roster. Each defendant block opens with
# "Defendant (N)", followed by the name, zero or more "also known as" lines,
# and a "represented by" attorney block. Counsel is the trap: an unstructured
# pass over this block promotes the first attorney name to principal.
PACER_DEFENDANT_BLOCK_RE = re.compile(
    r"Defendant\s*\((?P<number>\d{1,2})\)\s*\n(?P<body>.*?)(?=\nDefendant\s*\(\d{1,2}\)|\nPlaintiff\b|\Z)",
    re.DOTALL,
)
PACER_AKA_RE = re.compile(r"also known as\s*\n\s*(?P<alias>[^\n]{1,60})")
PACER_REPRESENTED_BY_RE = re.compile(r"represented by\s+(?P<counsel>[^\n]{1,80})")
PACER_COUNSEL_CONTINUATION_RE = re.compile(
    r"^(?:LEAD ATTORNEY|ATTORNEY TO BE NOTICED|PRO HAC VICE|Designation:|Email:|Fax:|Ste\b|Suite\b)",
    re.IGNORECASE,
)
# Firm and address lines share the title-case shape of an attorney name.
PACER_LAW_FIRM_RE = re.compile(
    r"\b(?:PLLC|PLC|LLP|LLC|P\.?C\.?|INC\.?|CO\.?|Law|Offices?|Of[fﬁ]ices?|Associates|Group|Partners|Firm|Center|Defenders?|Society|Box)\b|&",
    re.IGNORECASE,
)
# Docket entry 1 count matrix: "Name (N) count(s) 1, 2, 3,".
PACER_COUNT_MATRIX_RE = re.compile(
    r"(?P<name>[A-Z][A-Za-z.'\-]+(?:\s+[A-Z][A-Za-z.'\-]+){0,3})\s*\((?P<number>\d{1,2})\)\s*count\(s\)\s*(?P<counts>[\d,\s]+)"
)


@dataclass(frozen=True)
class SemanticEntity:
    """One reviewable ontology mapping anchored in canonical section text."""

    ontology_class: str
    label: str
    matched_text: str
    start: int
    end: int
    section_id: str = "s1"
    graph_facets: tuple[dict[str, Any], ...] = ()
    extra_properties: dict[str, Any] = field(default_factory=dict)


def _anchor(section_id: str, start: int, end: int, exact: str) -> dict[str, Any]:
    return {
        "selector_kind": "text_position",
        "section_id": section_id,
        "start": start,
        "end": end,
        "exact": exact,
    }


def _facet_id(run_seed: str, kind: str) -> str:
    return f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, f'{run_seed}:{kind}')}"


def _is_plausible_locality(locality: str) -> bool:
    tokens = [token.lower() for token in re.split(r"\s+", locality.strip()) if token]
    if not tokens:
        return False
    if all(token in LOCATION_STOPWORDS for token in tokens):
        return False
    if tokens[0] in {"the", "a", "an"}:
        return False
    return True


def _person_label(first: str, last: str, alias: str | None = None) -> str:
    full = f"{first} {last}".strip()
    if alias:
        return f"{full} (aka {alias})"
    return full


def _add_person_match(
    matches: list[SemanticEntity],
    seen_spans: set[tuple[int, int, str]],
    seen_people: set[tuple[str, str]],
    *,
    first: str,
    last: str,
    matched_text: str,
    start: int,
    end: int,
    section_id: str,
    run_seed: str,
    alias: str | None = None,
) -> None:
    person_key = (first.lower(), last.lower())
    if person_key in seen_people:
        return
    seen_people.add(person_key)
    label = _person_label(first, last, alias)
    _add_match(
        matches,
        seen_spans,
        ontology_class="uco-identity:Person",
        label=label[:120],
        matched_text=matched_text,
        start=start,
        end=end,
        section_id=section_id,
        run_seed=run_seed,
        extra_properties={
            "uco-core:description": f"Person referenced in document text: {label}.",
        },
    )


def _add_display_name_person(
    matches: list[SemanticEntity],
    seen_spans: set[tuple[int, int, str]],
    seen_people: set[tuple[str, str]],
    *,
    display_name: str,
    matched_text: str,
    start: int,
    end: int,
    section_id: str,
    run_seed: str,
    alias: str | None = None,
) -> None:
    parts = [part for part in display_name.split() if part]
    if len(parts) >= 2 and not any(
        part.lower() in PERSON_NAME_STOPWORDS for part in parts
    ):
        _add_person_match(
            matches,
            seen_spans,
            seen_people,
            first=parts[0],
            last=parts[-1],
            alias=alias,
            matched_text=matched_text,
            start=start,
            end=end,
            section_id=section_id,
            run_seed=run_seed,
        )
        return
    label = display_name if not alias else f"{display_name} (aka {alias})"
    _add_match(
        matches,
        seen_spans,
        ontology_class="uco-identity:Person",
        label=label[:120],
        matched_text=matched_text,
        start=start,
        end=end,
        section_id=section_id,
        run_seed=run_seed,
        extra_properties={
            "uco-core:description": f"Person referenced in document text: {label}.",
        },
    )


def _person_name_span(value_col: str, row_start: int, row_end: int, full_text: str) -> tuple[str, str, str | None, int, int] | None:
    aka_match = PERSON_AKA_RE.search(value_col)
    if aka_match:
        first, last, alias = aka_match.group(1), aka_match.group(2), aka_match.group(3)
        name_text = f"{first} {last}"
        name_start = full_text.find(name_text, row_start, row_end)
        if name_start < 0:
            return None
        return first, last, alias, name_start, name_start + len(name_text)
    simple_match = re.match(
        r"^(?:Special Agent\s+)?([A-Z][a-z]+)\s+([A-Z][a-z]+)\b",
        value_col.strip(),
    )
    if not simple_match:
        return None
    first, last = simple_match.group(1), simple_match.group(2)
    if first.lower() in PERSON_NAME_STOPWORDS or last.lower() in PERSON_NAME_STOPWORDS:
        return None
    name_text = f"{first} {last}"
    name_start = full_text.find(name_text, row_start, row_end)
    if name_start < 0:
        return None
    return first, last, None, name_start, name_start + len(name_text)


def _add_match(
    matches: list[SemanticEntity],
    seen_spans: set[tuple[int, int, str]],
    *,
    ontology_class: str,
    label: str,
    matched_text: str,
    start: int,
    end: int,
    section_id: str,
    run_seed: str,
    facets: tuple[dict[str, Any], ...] = (),
    extra_properties: dict[str, Any] | None = None,
) -> None:
    key = (start, end, ontology_class)
    if key in seen_spans or not matched_text.strip():
        return
    seen_spans.add(key)
    matches.append(
        SemanticEntity(
            ontology_class=ontology_class,
            label=label[:120],
            matched_text=matched_text,
            start=start,
            end=end,
            section_id=section_id,
            graph_facets=facets or (),
            extra_properties=extra_properties or {},
        )
    )


def extract_semantic_entities(
    full_text: str,
    *,
    section_id: str = "s1",
    run_seed: str = "semantic",
) -> list[SemanticEntity]:
    """Map bounded high-confidence spans in ``full_text`` to CASE/UCO classes."""

    if not full_text.strip():
        return []

    matches: list[SemanticEntity] = []
    seen_spans: set[tuple[int, int, str]] = set()
    seen_people: set[tuple[str, str]] = set()

    for match in EMAIL_RE.finditer(full_text):
        value = match.group(0)
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-observable:EmailAddress",
            label=f"Email {value}",
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            facets=(
                {
                    "@id": _facet_id(run_seed, f"email-{match.start()}"),
                    "@type": "uco-observable:EmailAddressFacet",
                    "uco-observable:addressValue": value,
                },
            ),
        )

    for match in PHONE_RE.finditer(full_text):
        value = match.group(0).strip()
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-observable:PhoneAccount",
            label=f"Phone {value}",
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            facets=(
                {
                    "@id": _facet_id(run_seed, f"phone-{match.start()}"),
                    "@type": "uco-observable:PhoneAccountFacet",
                    "uco-observable:accountIdentifier": value,
                },
            ),
        )

    for match in URL_RE.finditer(full_text):
        value = match.group(0).rstrip(".,;)")
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-observable:URL",
            label=f"URL {value[:60]}",
            matched_text=value,
            start=match.start(),
            end=match.start() + len(value),
            section_id=section_id,
            run_seed=run_seed,
            facets=(
                {
                    "@id": _facet_id(run_seed, f"url-{match.start()}"),
                    "@type": "uco-observable:URLFacet",
                    "uco-observable:fullValue": value,
                },
            ),
        )

    # One node per distinct date. A filing stamp such as "Filed 12/02/25"
    # repeats on every page, and every count of an indictment re-states the
    # same offence dates, so per-mention nodes measure page count rather than
    # timeline. The first mention carries the anchor.
    seen_dates: set[str] = set()
    for match in DATE_RE.finditer(full_text):
        value = match.group(0)
        normalised = re.sub(r"\s+", " ", value).strip().casefold()
        if normalised in seen_dates:
            continue
        seen_dates.add(normalised)
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-core:Event",
            label=f"Date {value}",
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            extra_properties={
                "uco-core:eventType": ["document date reference"],
                "uco-core:description": f"Date reference in document text: {value}",
            },
        )

    for match in MONEY_RE.finditer(full_text):
        value = match.group(0).replace(" ", "")
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-observable:ObservableObject",
            label=f"Amount {value}",
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            extra_properties={
                "uco-core:description": f"Monetary amount referenced in document text: {value}",
            },
        )

    for match in HEADLINE_SUBJECT_RE.finditer(full_text):
        age = match.group(1)
        locality = match.group(2).strip()
        gender = match.group(3)
        span_text = match.group(0)
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-identity:Person",
            label=f"Subject ({age}-year-old {gender.lower()})",
            matched_text=span_text,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            extra_properties={
                "uco-core:description": (
                    f"Person described in document text ({age}-year-old {gender.lower()})."
                ),
            },
        )
        if locality and locality.lower() not in {"man", "woman", "male", "female"}:
            loc_start = full_text.find(locality, match.start(), match.end())
            if loc_start >= 0:
                _add_match(
                    matches,
                    seen_spans,
                    ontology_class="uco-location:Location",
                    label=f"Location {locality}",
                    matched_text=locality,
                    start=loc_start,
                    end=loc_start + len(locality),
                    section_id=section_id,
                    run_seed=run_seed,
                    facets=(
                        {
                            "@id": _facet_id(run_seed, f"loc-{loc_start}"),
                            "@type": "uco-location:SimpleAddressFacet",
                            "uco-location:locality": locality,
                        },
                    ),
                )

    for match in ORGANIZATION_RE.finditer(full_text):
        value = re.sub(r"\s+", " ", match.group(0)).strip()
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-identity:Organization",
            label=value[:120],
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
        )

    for match in LOCATION_RE.finditer(full_text):
        locality = None
        loc_start = match.start()
        loc_end = match.end()
        for group_index in range(1, (match.lastindex or 0) + 1):
            group_value = match.group(group_index)
            if group_value:
                locality = group_value.strip()
                loc_start = match.start(group_index)
                loc_end = match.end(group_index)
                break
        if not locality or not _is_plausible_locality(locality):
            continue
        if locality.lower() in {"man", "woman", "the", "his", "her"}:
            continue
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-location:Location",
            label=f"Location {locality}",
            matched_text=locality,
            start=loc_start,
            end=loc_end,
            section_id=section_id,
            run_seed=run_seed,
            facets=(
                {
                    "@id": _facet_id(run_seed, f"loc2-{loc_start}"),
                    "@type": "uco-location:SimpleAddressFacet",
                    "uco-location:locality": locality,
                },
            ),
        )

    for match in US_STREET_ADDRESS_RE.finditer(full_text):
        street = match.group(1).strip()
        locality = match.group(2).strip()
        region = match.group(3).strip()
        postal = match.group(4).strip()
        value = match.group(0).strip("*")
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-location:Location",
            label=f"Address {street}, {locality}",
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            facets=(
                {
                    "@id": _facet_id(run_seed, f"addr-{match.start()}"),
                    "@type": "uco-location:SimpleAddressFacet",
                    "uco-location:street": street,
                    "uco-location:locality": locality,
                    "uco-location:region": region,
                    "uco-location:postalCode": postal,
                },
            ),
        )

    for match in BOLD_PERSON_NAME_RE.finditer(full_text):
        raw = match.group(1).strip()
        if "(" in raw:
            raw = raw.split("(", 1)[0].strip()
        parts = raw.split()
        if len(parts) < 2:
            continue
        if any(part.lower() in PERSON_NAME_STOPWORDS for part in parts):
            continue
        first, last = parts[0], parts[-1]
        _add_person_match(
            matches,
            seen_spans,
            seen_people,
            first=first,
            last=last,
            matched_text=match.group(0).strip("*"),
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
        )

    for match in PERSON_AKA_RE.finditer(full_text):
        first, last, alias = match.group(1), match.group(2), match.group(3)
        if first.lower() in PERSON_NAME_STOPWORDS or last.lower() in PERSON_NAME_STOPWORDS:
            continue
        _add_person_match(
            matches,
            seen_spans,
            seen_people,
            first=first,
            last=last,
            alias=alias,
            matched_text=match.group(0),
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
        )

    for match in PERSON_OF_RE.finditer(full_text):
        first, last = match.group(1), match.group(2)
        if first.lower() in PERSON_NAME_STOPWORDS or last.lower() in PERSON_NAME_STOPWORDS:
            continue
        _add_person_match(
            matches,
            seen_spans,
            seen_people,
            first=first,
            last=last,
            matched_text=f"{first} {last}",
            start=match.start(1),
            end=match.end(2),
            section_id=section_id,
            run_seed=run_seed,
        )

    for match in ROLE_TABLE_PERSON_RE.finditer(full_text):
        first, last = match.group(1), match.group(2)
        alias = match.group(3)
        if first.lower() in PERSON_NAME_STOPWORDS or last.lower() in PERSON_NAME_STOPWORDS:
            continue
        _add_person_match(
            matches,
            seen_spans,
            seen_people,
            first=first,
            last=last,
            alias=alias,
            matched_text=f"{first} {last}",
            start=match.start(1),
            end=match.end(2),
            section_id=section_id,
            run_seed=run_seed,
        )

    for match in MARKDOWN_TABLE_ROW_RE.finditer(full_text):
        if MARKDOWN_TABLE_SEPARATOR_RE.match(match.group(0)):
            continue
        label_col = match.group(1).strip()
        value_col = match.group(2).strip()
        if label_col.lower() in TABLE_HEADER_LABELS:
            continue
        parsed = _person_name_span(
            value_col,
            match.start(),
            match.end(),
            full_text,
        )
        if not parsed:
            continue
        first, last, alias, name_start, name_end = parsed
        _add_person_match(
            matches,
            seen_spans,
            seen_people,
            first=first,
            last=last,
            alias=alias,
            matched_text=full_text[name_start:name_end],
            start=name_start,
            end=name_end,
            section_id=section_id,
            run_seed=run_seed,
        )

    for match in CHAT_SPEAKER_LINE_RE.finditer(full_text):
        display_name = match.group(1).strip()
        handle = match.group(2)
        display_start = match.start(1)
        display_end = match.end(1)
        _add_display_name_person(
            matches,
            seen_spans,
            seen_people,
            display_name=display_name,
            matched_text=display_name,
            start=display_start,
            end=display_end,
            section_id=section_id,
            run_seed=run_seed,
        )
        handle_text = f"@{handle}"
        handle_start = full_text.find(handle_text, match.start(), match.end())
        if handle_start >= 0:
            _add_match(
                matches,
                seen_spans,
                ontology_class="uco-observable:InstantMessagingAddress",
                label=f"Telegram {handle_text}",
                matched_text=handle_text,
                start=handle_start,
                end=handle_start + len(handle_text),
                section_id=section_id,
                run_seed=run_seed,
                facets=(
                    {
                        "@id": _facet_id(run_seed, f"im-chat-{handle_start}"),
                        "@type": "uco-observable:InstantMessagingAddressFacet",
                        "uco-observable:addressValue": handle_text,
                    },
                ),
                extra_properties={
                    "uco-core:description": (
                        f"Instant messaging handle for chat speaker {display_name}."
                    ),
                },
            )

    for match in ACCOUNT_HOLDER_RE.finditer(full_text):
        first, last = match.group(1), match.group(2)
        if first.lower() in PERSON_NAME_STOPWORDS or last.lower() in PERSON_NAME_STOPWORDS:
            continue
        _add_person_match(
            matches,
            seen_spans,
            seen_people,
            first=first,
            last=last,
            matched_text=f"{first} {last}",
            start=match.start(1),
            end=match.end(2),
            section_id=section_id,
            run_seed=run_seed,
        )

    for match in TELEGRAM_HANDLE_RE.finditer(full_text):
        handle = f"@{match.group(1)}"
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-observable:InstantMessagingAddress",
            label=f"Telegram {handle}",
            matched_text=handle,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            facets=(
                {
                    "@id": _facet_id(run_seed, f"im-{match.start()}"),
                    "@type": "uco-observable:InstantMessagingAddressFacet",
                    "uco-observable:addressValue": handle,
                },
            ),
            extra_properties={
                "uco-core:description": "Instant messaging handle referenced in document text.",
            },
        )

    for match in ETH_WALLET_RE.finditer(full_text):
        value = match.group(1)
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-observable:ObservableObject",
            label=f"Ethereum wallet {value[:10]}…",
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            extra_properties={
                "uco-core:description": f"Ethereum wallet address referenced in document text: {value}",
            },
        )

    for match in TRON_WALLET_RE.finditer(full_text):
        value = match.group(1)
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-observable:ObservableObject",
            label=f"Tron wallet {value[:10]}…",
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            extra_properties={
                "uco-core:description": f"Tron wallet address referenced in document text: {value}",
            },
        )

    for match in DOMAIN_HOST_RE.finditer(full_text):
        value = match.group(1)
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-observable:DomainName",
            label=f"Domain {value}",
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            extra_properties={
                "uco-core:description": f"Domain referenced in document text: {value}",
            },
        )

    # Every page of a PACER PDF repeats the case number and the
    # "Case ... Document N Filed ..." stamp in its header. Emitting one Event
    # per occurrence buries the real docket entries under dozens of identical
    # header nodes, so each case number and document number is emitted once,
    # anchored at its first occurrence.
    seen_case_numbers: set[str] = set()
    for match in PACER_CASE_NUMBER_RE.finditer(full_text):
        value = match.group(1)
        if value.casefold() in seen_case_numbers:
            continue
        seen_case_numbers.add(value.casefold())
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-core:Event",
            label=f"Federal case {value}",
            matched_text=match.group(0),
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            extra_properties={
                "uco-core:eventType": ["federal court case reference"],
                "uco-core:description": f"PACER/ECF case number: {value}",
            },
        )

    seen_documents: set[str] = set()
    for match in PACER_ECF_DOCUMENT_RE.finditer(full_text):
        doc_num, filed = match.group(1), match.group(2)
        if doc_num in seen_documents:
            continue
        seen_documents.add(doc_num)
        value = match.group(0)
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-core:Event",
            label=f"PACER filing Document {doc_num}",
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            extra_properties={
                "uco-core:eventType": ["pacer docket filing"],
                "uco-core:description": (
                    f"PACER document {doc_num} filed {filed}."
                ),
            },
        )

    for match in FEDERAL_STATUTE_RE.finditer(full_text):
        value = re.sub(r"\s+", " ", match.group(0)).strip()
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-observable:ObservableObject",
            label=f"Statute {value[:80]}",
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            extra_properties={
                "uco-core:description": f"Federal statute citation in document text: {value}",
            },
        )

    for match in USC_SECTION_PROSE_RE.finditer(full_text):
        title, section = match.group(1), match.group(2)
        value = f"{title} U.S.C. § {section}"
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-observable:ObservableObject",
            label=f"Statute {value[:80]}",
            matched_text=match.group(0),
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            extra_properties={
                "uco-core:description": f"Federal statute citation in document text: {value}",
            },
        )

    seen_counts: set[str] = set()
    for match in INDICTMENT_COUNT_RE.finditer(full_text):
        count_num = match.group(1)
        if count_num in seen_counts:
            continue
        seen_counts.add(count_num)
        value = match.group(0)
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-core:Event",
            label=f"Indictment count {count_num}",
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            extra_properties={
                "uco-core:eventType": ["indictment count reference"],
                "uco-core:description": f"Numbered count in charging instrument: {value}",
            },
        )

    for match in FEDERAL_DEFENDANT_AKA_RE.finditer(full_text):
        raw_name, alias = match.group(1), match.group(2).strip().rstrip(",")
        parts = raw_name.split()
        if len(parts) < 2:
            continue
        first = parts[0].title()
        last = parts[-1].title()
        _add_person_match(
            matches,
            seen_spans,
            seen_people,
            first=first,
            last=last,
            alias=alias,
            matched_text=match.group(0),
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
        )

    # Identity resolution: one node per victim label. A charging instrument
    # names the same Minor Victim across many counts and paragraphs, and one
    # node per mention makes victim-linked queries count mentions, not victims.
    # The first mention carries the anchor.
    seen_victims: set[str] = set()
    for match in MINOR_VICTIM_RE.finditer(full_text):
        victim_num = match.group(1)
        if victim_num in seen_victims:
            continue
        seen_victims.add(victim_num)
        value = match.group(0)
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-identity:Person",
            label=f"Minor Victim {victim_num}",
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            extra_properties={
                "uco-core:description": (
                    f"Minor victim identifier in charging or trial document: {value}."
                ),
            },
        )

    seen_snapchat: set[str] = set()
    for pattern in (SNAPCHAT_ACCOUNT_RE, SNAPCHAT_USERNAME_RE):
        for match in pattern.finditer(full_text):
            handle = match.group(1)
            if handle.lower() in seen_snapchat:
                continue
            seen_snapchat.add(handle.lower())
            account_id = handle if handle.startswith("@") else handle
            _add_match(
                matches,
                seen_spans,
                ontology_class="uco-observable:ApplicationAccount",
                label=f"Snapchat {account_id}",
                matched_text=match.group(0),
                start=match.start(),
                end=match.end(),
                section_id=section_id,
                run_seed=run_seed,
                facets=(
                    {
                        "@id": _facet_id(run_seed, f"snap-{match.start()}"),
                        "@type": "uco-observable:AccountFacet",
                        "uco-observable:accountIdentifier": account_id,
                    },
                ),
                extra_properties={
                    "uco-core:description": (
                        f"Snapchat account referenced in document text: {account_id}."
                    ),
                },
            )

    seen_platforms: set[tuple[str, str]] = set()
    for match in PLATFORM_ACCOUNT_RE.finditer(full_text):
        platform = match.group("platform").title()
        raw_handle = match.group("handle")
        marked = bool(match.group("marker")) or bool(match.group("quote")) or raw_handle.startswith("@")
        if not _is_plausible_account_handle(raw_handle, marked):
            continue
        handle = raw_handle.lstrip("@")
        key = (platform.lower(), handle.lower())
        if key in seen_platforms or (
            platform.lower() == "snapchat" and handle.lower() in seen_snapchat
        ):
            continue
        seen_platforms.add(key)
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-observable:ApplicationAccount",
            label=f"{platform} {handle}",
            matched_text=match.group(0),
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            facets=(
                {
                    "@id": _facet_id(run_seed, f"acct-{platform}-{match.start()}"),
                    "@type": "uco-observable:AccountFacet",
                    "uco-observable:accountIdentifier": handle,
                },
            ),
            extra_properties={
                "uco-core:description": (
                    f"{platform} account referenced in document text: {handle}."
                ),
            },
        )

    for match in US_V_CAPTION_RE.finditer(full_text):
        raw_name = re.sub(r"\s+", " ", match.group(1)).strip(" ,")
        parts = [p for p in raw_name.split() if p.isalpha() or p.replace(".", "").isalpha()]
        if len(parts) < 2:
            continue
        _add_person_match(
            matches,
            seen_spans,
            seen_people,
            first=parts[0].title(),
            last=parts[-1].title(),
            matched_text=match.group(0)[:200],
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
        )

    seen_tools: set[str] = set()
    for match in FORENSIC_TOOL_RE.finditer(full_text):
        name = re.sub(r"\s+", " ", match.group(1)).strip()
        key = name.casefold()
        if key in seen_tools:
            continue
        seen_tools.add(key)
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-tool:Tool",
            label=name,
            matched_text=match.group(0),
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            extra_properties={
                "uco-core:name": name,
                "uco-core:description": (
                    f"Digital forensics tool named in the filing: {name}."
                ),
            },
        )

    for match in FEDERAL_DISTRICT_RE.finditer(full_text):
        district = match.group(1).strip().title()
        if not district or district.lower() in LOCATION_STOPWORDS:
            continue
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-location:Location",
            label=f"District of {district}",
            matched_text=match.group(0).strip(),
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            facets=(
                {
                    "@id": _facet_id(run_seed, f"district-{match.start()}"),
                    "@type": "uco-location:SimpleAddressFacet",
                    "uco-location:region": f"District of {district}",
                },
            ),
            extra_properties={
                "uco-core:description": (
                    f"Federal judicial district referenced in document text: District of {district}."
                ),
            },
        )

    charge_match = CHARGE_NARRATIVE_RE.search(full_text)
    if charge_match:
        window_start = max(0, charge_match.start() - 80)
        window_end = min(len(full_text), charge_match.end() + 120)
        window_text = full_text[window_start:window_end]
        narrative = window_text.strip()
        if narrative:
            lead_ws = window_text.index(narrative)
            anchored_start = window_start + lead_ws
            anchored_end = anchored_start + len(narrative)
            _add_match(
                matches,
                seen_spans,
                ontology_class="uco-core:Event",
                label="Law-enforcement charge or arrest narrative",
                matched_text=narrative[:400],
                start=anchored_start,
                end=min(anchored_end, anchored_start + 400),
                section_id=section_id,
                run_seed=run_seed,
                extra_properties={
                    "uco-core:eventType": ["criminal charge", "law-enforcement narrative"],
                    "uco-core:description": narrative[:500],
                },
            )

    # Stable ordering for deterministic graphs and tests.
    matches.sort(key=lambda item: (item.start, item.end, item.ontology_class, item.label))
    return matches[:MAX_SEMANTIC_ENTITIES]


def normalize_statute_citation(raw: str) -> str:
    """Collapse whitespace in a sourced federal citation."""

    text = re.sub(r"\s+", " ", raw).strip()
    text = text.replace("§§", "§")
    text = re.sub(r"U\.S\.C\.?", "U.S.C.", text, flags=re.IGNORECASE)
    text = re.sub(r"C\.F\.R\.?", "C.F.R.", text, flags=re.IGNORECASE)
    return text[:160]


def pair_counts_with_statutes(full_text: str) -> list[tuple[str, str]]:
    """Pair COUNT N headings with the first statute in that count block."""

    pairs: list[tuple[str, str]] = []
    starts = list(INDICTMENT_COUNT_RE.finditer(full_text))
    for index, match in enumerate(starts):
        count_num = match.group(1)
        block_end = starts[index + 1].start() if index + 1 < len(starts) else min(
            len(full_text), match.end() + 800
        )
        block = full_text[match.end() : block_end]
        usc = FEDERAL_STATUTE_RE.search(block)
        prose = USC_SECTION_PROSE_RE.search(block)
        if usc is not None:
            citation = usc.group(0)
        elif prose is not None:
            citation = f"{prose.group(1)} U.S.C. § {prose.group(2)}"
        else:
            continue
        pairs.append((count_num, normalize_statute_citation(citation)))
    return pairs


def extract_pacer_legal_facts(full_text: str) -> dict[str, Any]:
    """Unbounded PACER legal facts for Layer-2 case graphs.

    Layer-1 semantic mapping is capped. Charge, caption, tool, and
    sentence extraction for a docket graph must not drop later counts
    because an earlier email or date filled the cap.
    """

    case_numbers: list[str] = []
    seen_cases: set[str] = set()
    for match in PACER_CASE_NUMBER_RE.finditer(full_text):
        value = match.group(1)
        key = value.casefold()
        if key in seen_cases:
            continue
        seen_cases.add(key)
        case_numbers.append(value)

    statutes: list[str] = []
    seen_statutes: set[str] = set()
    for match in FEDERAL_STATUTE_RE.finditer(full_text):
        value = normalize_statute_citation(match.group(0))
        if value.casefold() in seen_statutes:
            continue
        seen_statutes.add(value.casefold())
        statutes.append(value)
    for match in USC_SECTION_PROSE_RE.finditer(full_text):
        value = normalize_statute_citation(f"{match.group(1)} U.S.C. § {match.group(2)}")
        if value.casefold() in seen_statutes:
            continue
        seen_statutes.add(value.casefold())
        statutes.append(value)

    counts: list[str] = []
    seen_counts: set[str] = set()
    for match in INDICTMENT_COUNT_RE.finditer(full_text):
        if match.group(1) in seen_counts:
            continue
        seen_counts.add(match.group(1))
        counts.append(match.group(1))

    defendants: list[str] = []
    seen_defendants: set[str] = set()
    for match in FEDERAL_DEFENDANT_AKA_RE.finditer(full_text):
        raw_name, alias = match.group(1), match.group(2).strip().rstrip(",")
        parts = raw_name.split()
        if len(parts) < 2:
            continue
        label = f"{parts[0].title()} {parts[-1].title()} (aka {alias})"
        if label.casefold() in seen_defendants:
            continue
        seen_defendants.add(label.casefold())
        defendants.append(label)
    for match in US_V_CAPTION_RE.finditer(full_text):
        raw_name = re.sub(r"\s+", " ", match.group(1)).strip(" ,")
        parts = [p for p in raw_name.split() if p.replace(".", "").isalpha()]
        if len(parts) < 2:
            continue
        label = f"{parts[0].title()} {parts[-1].title()}"
        if label.casefold() in seen_defendants:
            continue
        seen_defendants.add(label.casefold())
        defendants.append(label)

    tools: list[str] = []
    seen_tools: set[str] = set()
    for match in FORENSIC_TOOL_RE.finditer(full_text):
        name = re.sub(r"\s+", " ", match.group(1)).strip()
        if name.casefold() in seen_tools:
            continue
        seen_tools.add(name.casefold())
        tools.append(name)

    method_claims: list[dict[str, str]] = []
    if FORENSIC_IMAGE_METHOD_RE.search(full_text):
        method_claims.append(
            {
                "phrase": "forensic image or bitstream copy",
                "technique_id": "DFT-1002",
            }
        )
    if MOBILE_EXTRACTION_METHOD_RE.search(full_text):
        method_claims.append(
            {
                "phrase": "mobile or file-system extraction",
                "technique_id": "DFT-1020",
            }
        )
    if PHOTO_DNA_MATCH_RE.search(full_text):
        method_claims.append(
            {
                "phrase": "PhotoDNA hash match",
                "technique_id": "DFT-1050",
            }
        )

    platforms: list[dict[str, str]] = []
    seen_platforms: set[tuple[str, str]] = set()
    for match in PLATFORM_ACCOUNT_RE.finditer(full_text):
        platform = match.group("platform").title()
        raw_handle = match.group("handle")
        marked = bool(match.group("marker")) or bool(match.group("quote")) or raw_handle.startswith("@")
        if not _is_plausible_account_handle(raw_handle, marked):
            continue
        handle = raw_handle.lstrip("@")
        key = (platform.lower(), handle.lower())
        if key in seen_platforms:
            continue
        seen_platforms.add(key)
        platforms.append({"platform": platform, "account_identifier": handle})

    filings: list[dict[str, str]] = []
    seen_filings: set[str] = set()
    for match in PACER_ECF_DOCUMENT_RE.finditer(full_text):
        doc_num, filed = match.group(1), match.group(2)
        if doc_num in seen_filings:
            continue
        seen_filings.add(doc_num)
        filings.append({"document_number": doc_num, "filed": filed})

    districts: list[str] = []
    for match in FEDERAL_DISTRICT_RE.finditer(full_text):
        district = match.group(1).strip().title()
        if district and district.lower() not in LOCATION_STOPWORDS:
            label = f"District of {district}"
            if label not in districts:
                districts.append(label)

    victims: list[str] = []
    for match in MINOR_VICTIM_RE.finditer(full_text):
        label = f"Minor Victim {match.group(1)}"
        if label not in victims:
            victims.append(label)

    custody: list[str] = []
    for match in IMPOSED_CUSTODY_RE.finditer(full_text):
        term = re.sub(r"\s+", " ", match.group(1)).strip().lower()
        if term not in custody:
            custody.append(term)

    supervised: list[str] = []
    for match in SUPERVISED_RELEASE_TERM_RE.finditer(full_text):
        term = re.sub(r"\s+", " ", match.group(1)).strip().lower()
        if term not in supervised:
            supervised.append(term)

    return {
        "case_numbers": case_numbers,
        "statutes": statutes,
        "counts": counts,
        "count_statutes": pair_counts_with_statutes(full_text),
        "defendants": defendants,
        "minor_victims": victims,
        "tools": tools,
        "method_claims": method_claims,
        "platforms": platforms,
        "filings": filings,
        "districts": districts,
        "custody_terms": custody,
        "supervised_release_terms": supervised,
        "plea_guilty": bool(GUILTY_PLEA_RE.search(full_text)),
    }


def extract_pacer_docket_roster(full_text: str) -> dict[str, Any]:
    """Parse the PACER criminal docket roster structurally.

    Returns the defendant roster (number, name, aliases, counsel) and the
    docket-entry-1 count matrix. Layer-2 synthesis should read defendants and
    per-defendant counts from here rather than from the general NER pass: the
    "represented by" attorney block sits inside each defendant block, and a
    string-level reading promotes counsel to principal.

    Aliases and counsel are reported separately so a caller can never confuse
    them with the charged party. An empty roster means the document is not a
    PACER docket sheet, not that there are no defendants.
    """

    roster: list[dict[str, Any]] = []
    for block in PACER_DEFENDANT_BLOCK_RE.finditer(full_text):
        body = block.group("body")
        lines = [line.strip() for line in body.splitlines()]
        name = next((line for line in lines if line), "")
        # The charged party is the first line of the block, before any
        # "also known as" or "represented by" marker.
        if not name or name.lower().startswith(("also known as", "represented by")):
            continue

        aliases = [m.group("alias").strip() for m in PACER_AKA_RE.finditer(body)]
        aliases = [alias for alias in aliases if alias and not alias.startswith("represented by")]

        counsel: list[str] = []
        represented = PACER_REPRESENTED_BY_RE.search(body)
        if represented:
            counsel.append(represented.group("counsel").strip())
            # Additional attorneys appear as bare name lines after the first
            # attorney's contact block and before "Pending Counts".
            tail = body[represented.end() :]
            for line in tail.splitlines():
                line = line.strip()
                if line.startswith("Pending Counts"):
                    break
                if not line or PACER_COUNSEL_CONTINUATION_RE.match(line):
                    continue
                if PACER_LAW_FIRM_RE.search(line):
                    continue
                parts = line.split()
                if 2 <= len(parts) <= 4 and all(
                    part[:1].isupper() for part in parts if part[:1].isalpha()
                ):
                    if not any(char.isdigit() for char in line) and line not in counsel:
                        counsel.append(line)

        roster.append(
            {
                "defendant_number": int(block.group("number")),
                "name": name,
                "aliases": aliases,
                "counsel": counsel,
            }
        )

    count_matrix: list[dict[str, Any]] = []
    seen_numbers: set[int] = set()
    for match in PACER_COUNT_MATRIX_RE.finditer(full_text):
        number = int(match.group("number"))
        if number in seen_numbers:
            continue
        counts = sorted(
            {int(value) for value in re.findall(r"\d+", match.group("counts"))}
        )
        if not counts:
            continue
        seen_numbers.add(number)
        count_matrix.append(
            {
                "defendant_number": number,
                "name": re.sub(r"\s+", " ", match.group("name")).strip(),
                "counts": counts,
            }
        )

    counsel_names = sorted({name for entry in roster for name in entry["counsel"]})
    return {
        "defendants": roster,
        "count_matrix": sorted(count_matrix, key=lambda entry: entry["defendant_number"]),
        "counsel_names": counsel_names,
    }


def semantic_entities_to_records(
    entities: list[SemanticEntity],
) -> list[ExtractedRecord]:
    """Convert semantic entities into ``ExtractedRecord`` instances."""

    records: list[ExtractedRecord] = []
    for entity in entities:
        records.append(
            ExtractedRecord(
                label=entity.label,
                text=entity.matched_text[:400],
                anchor=_anchor(entity.section_id, entity.start, entity.end, entity.matched_text[:400]),
                ontology_class=entity.ontology_class,
                graph_facets=entity.graph_facets,
                extra_properties=entity.extra_properties,
            )
        )
    return records
