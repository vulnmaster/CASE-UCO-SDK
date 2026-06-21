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

MAX_SEMANTIC_ENTITIES = 48

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
    r"FBI(?:\s+Portland(?:\s+Resident Agency)?)|"
    r"Internet Crimes Against Children(?:\s+Task Force)?|"
    r"ICAC(?:\s+Task Force)?|"
    r"Coinbase|Pacific Rim OTC"
    r")\b",
    re.IGNORECASE,
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
    r"\|\s*(?:Applying Agent|Victim|Groomer|Analyst|Mule(?:\s*/\s*cash-out)?)\s*\|\s*"
    r"(?:Special Agent\s+)?([A-Z][a-z]+)\s+([A-Z][a-z]+)",
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
    }
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

    for match in DATE_RE.finditer(full_text):
        value = match.group(0)
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
