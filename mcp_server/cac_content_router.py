"""Route incoming content to one or more CAC Ontology modeling recipes.

Hermes, Link-Look, and other MCP callers submit free text, structured
artifacts, document paths, or partial CASE/UCO/CAC graphs. This module
scores the submission against CAC domain families and returns multiple
matching recipes plus validation guidance. Guidance-only: callers (or
their agents) build the graph; the SDK validates it afterward.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from domain_index import MAPPING_GUIDE_INDEX, RECIPE_INDEX

GRAPH_EXTENSIONS = {".json", ".jsonld", ".json-ld", ".ttl", ".turtle"}
DOCUMENT_EXTENSIONS = {
    ".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".tiff",
    ".docx", ".xlsx", ".csv", ".tsv", ".txt", ".md",
}
CAC_IRI_MARKERS = (
    "cacontology.projectvic.org",
    "cacontology:",
    "cac-core:",
)
MIN_DOMAIN_SCORE = 2
MAX_RECIPE_CONTENT_CHARS = 8000


@dataclass(frozen=True)
class CACDomainFamily:
    """One CAC case-family routing entry."""

    domain_id: str
    title: str
    keywords: tuple[str, ...]
    recipe_file: str
    mapping_source: str | None
    layer: int
    related_core_recipes: tuple[str, ...] = ()


CAC_DOMAIN_FAMILIES: tuple[CACDomainFamily, ...] = (
    CACDomainFamily(
        domain_id="grooming-chat",
        title="Online Grooming Chat Modeling",
        keywords=(
            "grooming", "groomed", "chat", "message", "snapchat", "discord",
            "secrecy", "sexual solicitation", "soliciting a minor",
            "solicitation of a minor", "sexually soliciting", "trust building",
            "isolation", "sexualization", "online predator", "enticement",
            "minor victim",
        ),
        recipe_file="docs/recipes/cac-grooming-chat-modeling.md",
        mapping_source="cybertip grooming report",
        layer=2,
        related_core_recipes=("docs/recipes/threaded-messaging.md",),
    ),
    CACDomainFamily(
        domain_id="cybertip-ncmec",
        title="NCMEC CyberTip Reporting Workflow",
        keywords=(
            "cybertip", "ncmec", "cybertipline", "2258a", "esp", "platform",
            "trust and safety", "automated detection", "report to ncmec",
            "investigation trigger", "platform cooperation", "electronic service provider",
        ),
        recipe_file="docs/recipes/cybertip-ncmec-workflow.md",
        mapping_source="cybertip grooming report",
        layer=3,
        related_core_recipes=(
            "docs/recipes/forensic-lifecycle.md",
            "docs/recipes/caselinker-icac-remodel.md",
        ),
    ),
    CACDomainFamily(
        domain_id="trafficking-recruitment",
        title="Child Sex Trafficking and Recruitment Networks",
        keywords=(
            "trafficking", "trafficker", "trafficked", "csec", "cse", "ring",
            "recruitment", "recruiter", "peer recruitment", "school-based",
            "street recruitment", "pretext", "rotation", "interstate transport",
            "digital-to-physical", "brooklyn trafficking",
            "1591", "sex trafficking a minor", "commercial sex act",
            "minor victim", "grindr", "victim transportation", "rideshare",
            "uber", "lyft", "hotel room", "commercial sexual exploitation",
        ),
        recipe_file="docs/recipes/cac-trafficking-recruitment-network.md",
        mapping_source="child sex trafficking prosecution or recruitment network",
        layer=2,
        related_core_recipes=(
            "docs/recipes/cac-grooming-chat-modeling.md",
            "docs/recipes/cac-federal-prosecution-relationships.md",
            "docs/recipes/cac-federal-trial-proceedings.md",
            "docs/recipes/cac-production-case.md",
        ),
    ),
    CACDomainFamily(
        domain_id="multi-jurisdiction-task-force",
        title="Multi-Jurisdictional Task Force Operations",
        keywords=(
            "task force", "taskforce", "icac", "multi-jurisdiction", "joint investigation",
            "joint operation", "mutual aid", "handoff", "hsi", "fbi", "interpol",
            "federal jurisdiction", "state jurisdiction", "mass rescue",
            "maryland state police", "computer crimes unit", "child exploitation unit",
            "governor's office", "governor's office of crime",
        ),
        recipe_file="docs/recipes/cac-multi-jurisdiction-task-force.md",
        mapping_source="multi-jurisdictional rescue or task force operation",
        layer=3,
        related_core_recipes=("docs/recipes/forensic-lifecycle.md",),
    ),
    CACDomainFamily(
        domain_id="victim-rescue-extraction",
        title="Victim Rescue, Extraction, and Post-Rescue Services",
        keywords=(
            "rescue", "extraction", "extract", "emergency response", "victim service",
            "safety planning", "trauma", "ongoing danger", "recantation", "dcfs",
            "child protective", "multi-agency victim", "welfare check",
        ),
        recipe_file="docs/recipes/cac-victim-rescue-extraction.md",
        mapping_source="victim rescue extraction and post-rescue services",
        layer=3,
        related_core_recipes=("docs/recipes/chain-of-custody.md",),
    ),
    CACDomainFamily(
        domain_id="icac-search-warrant-arrest",
        title="ICAC Search Warrant Arrest (Press Release Pattern)",
        keywords=(
            "search warrant", "executed a search warrant", "warrant arrest",
            "child exploitation unit", "without incident", "taken into custody",
            "custody without incident", "detention center", "held without bond",
            "anne arundel", "annapolis", "residence in", "transported to",
            "computer crimes unit", "internet crimes against children",
        ),
        recipe_file="docs/recipes/cac-icac-search-warrant-arrest.md",
        mapping_source="icac search warrant arrest",
        layer=3,
        related_core_recipes=(
            "docs/recipes/cac-multi-jurisdiction-task-force.md",
            "docs/recipes/cac-legal-sentencing-outcomes.md",
            "docs/recipes/cac-grooming-chat-modeling.md",
            "docs/recipes/caselinker-icac-remodel.md",
        ),
    ),
    CACDomainFamily(
        domain_id="tactical-undercover",
        title="Tactical Arrest and Undercover Operations",
        keywords=(
            "tactical", "high-risk", "dynamic entry", "swat", "raid",
            "undercover operation", "undercover sting", "sting operation",
            "asset forfeiture", "threat assessment", "coordinated arrest",
        ),
        recipe_file="docs/recipes/cac-tactical-undercover-operation.md",
        mapping_source="tactical arrest or high-risk operation",
        layer=3,
        related_core_recipes=("docs/recipes/forensic-lifecycle.md",),
    ),
    CACDomainFamily(
        domain_id="sextortion-coercion",
        title="Sextortion and Online Coercion",
        keywords=(
            "sextortion", "coercion", "blackmail", "threaten to share", "nude",
            "explicit images", "financial extortion", "compliance demand",
            "screenshot threat", "webcam", "catfish", "impersonation",
            "cyberstalking", "2261a", "wire fraud", "1343", "1028a",
            "aggravated identity theft", "ban evasion", "account recreation",
            "instagram", "snapchat", "dropbox",
        ),
        recipe_file="docs/recipes/cac-sextortion-coercion.md",
        mapping_source="cybertip grooming report or sextortion indictment",
        layer=2,
        related_core_recipes=(
            "docs/recipes/threaded-messaging.md",
            "docs/recipes/cac-grooming-chat-modeling.md",
            "docs/recipes/cac-federal-prosecution-relationships.md",
            "docs/recipes/cac-international-coordination.md",
        ),
    ),
    CACDomainFamily(
        domain_id="hotline-intake",
        title="Hotline Intake and Referral Lifecycle",
        keywords=(
            "hotline", "intake", "referral", "call center", "cybertipline intake",
            "report intake", "tip line", "childhelp", "national hotline",
            "victim referral", "mandatory reporting",
        ),
        recipe_file="docs/recipes/cac-hotline-intake-lifecycle.md",
        mapping_source=None,
        layer=3,
        related_core_recipes=("docs/recipes/cybertip-ncmec-workflow.md",),
    ),
    CACDomainFamily(
        domain_id="csam-forensic-provenance",
        title="CSAM Forensic Provenance and Victim Identification",
        keywords=(
            "csam", "child pornography", "child sexual abuse material",
            "child sex abuse material", "photodna", "perceptual hash", "hash match",
            "chain of custody", "forensic acquisition", "metadata correlation",
            "victim identification", "content hashing", "ai csam", "hash analysis",
            "purchasing operation", "csam purchasing", "child sex abuse material purchasing",
            "online purchase", "purchasing",
        ),
        recipe_file="docs/recipes/cac-csam-forensic-provenance.md",
        mapping_source="csam provenance forensics and victim identification",
        layer=1,
        related_core_recipes=(
            "docs/recipes/ai-analysis-pipeline.md",
            "docs/recipes/exif-data.md",
        ),
    ),
    CACDomainFamily(
        domain_id="legal-sentencing-outcomes",
        title="Legal Charges, Sentencing, and Case Outcomes",
        keywords=(
            "sentencing", "plea", "conviction", "indictment", "charges",
            "charged with", "statute", "supervised release", "registry",
            "sex offender registry", "legal outcome", "guilty", "prison sentence",
            "probation", "without bond", "held without bond", "detention center",
            "knowingly permitting",
        ),
        recipe_file="docs/recipes/cac-legal-sentencing-outcomes.md",
        mapping_source=None,
        layer=3,
        related_core_recipes=(
            "docs/recipes/event.md",
            "docs/recipes/caselinker-icac-remodel.md",
            "docs/recipes/legal-discovery-disclosure.md",
        ),
    ),
    CACDomainFamily(
        domain_id="federal-prosecution-relationships",
        title="Federal Prosecution Relationship Completeness",
        keywords=(
            "child exploitation enterprise", "2252a", "2252a(g)", "co-conspirator",
            "co-conspirators", "multi-defendant", "multi defendant", "superseding indictment",
            "federal charge", "federal prosecution", "federal defendant", "count 1",
            "count one", "numbered count", "conspiracy to commit", "conspiracy to produce",
            "district court", "u.s. v.", "united states v", "indictment filed",
            "enterprise member", "organized exploitation",
            "multi-district", "multi district", "parallel jurisdiction", "parallel prosecution",
            "western district", "district of alaska", "transportation of csam",
            "possession of csam", "receipt of csam", "production of csam",
            "sexual exploitation of a minor", "mobile recording device",
            "asset forfeiture", "forfeiture", "18 u.s.c. 2251", "18 u.s.c. 2252",
            "18 u.s.c. 2253", "pre-trial", "pretrial phase",
            "overt act", "violation one", "violation two", "judicial district",
            "southern district of california", "district of new mexico",
            "serial number", "forfeiture schedule",
            "cyberstalking", "2261a", "wire fraud", "1343", "1028a",
            "aggravated identity theft", "extradition", "extradited",
            "ban evasion", "impersonation",
        ),
        recipe_file="docs/recipes/cac-federal-prosecution-relationships.md",
        mapping_source="federal court prosecution indictment or criminal complaint",
        layer=3,
        related_core_recipes=(
            "docs/recipes/cac-legal-sentencing-outcomes.md",
            "docs/recipes/cac-production-case.md",
            "docs/recipes/cac-trafficking-recruitment-network.md",
            "docs/recipes/cac-federal-trial-proceedings.md",
        ),
    ),
    CACDomainFamily(
        domain_id="federal-trial-proceedings",
        title="Federal Trial Proceedings and Docket Lifecycle",
        keywords=(
            "superseding indictment", "superseding", "trial brief",
            "government trial brief", "pacer docket", "docket sheet",
            "competency hearing", "4241", "speedy trial act",
            "motion in limine", "jury trial", "jury selection",
            "trial conference", "anticipated evidence", "ecf no",
            "document 70", "arraignment continuance", "detention hearing",
        ),
        recipe_file="docs/recipes/cac-federal-trial-proceedings.md",
        mapping_source="federal docket export or government trial brief",
        layer=3,
        related_core_recipes=(
            "docs/recipes/cac-federal-prosecution-relationships.md",
            "docs/recipes/cac-csam-forensic-provenance.md",
            "docs/recipes/cac-legal-sentencing-outcomes.md",
        ),
    ),
    CACDomainFamily(
        domain_id="pacer-document-ingestion",
        title="PACER Document Ingestion (MCP Agent Workflow)",
        keywords=(
            "pacer", "ecf", "ao 245b", "usm number",
            "judgment in a criminal case", "-cr-0", "grand jury charges",
            "criminal forfeiture allegation", "special assessment",
            "schedule of payments", "supervised release for a term",
            "date of imposition of judgment", "sheet 3d", "special conditions",
            "process_document_file", "indictment.pdf", "judgment.pdf",
            "trial brief.pdf",
        ),
        recipe_file="docs/recipes/cac-pacer-document-ingestion.md",
        mapping_source="pacer pdf bundle (indictment, trial brief, judgment)",
        layer=3,
        related_core_recipes=(
            "docs/recipes/cac-federal-prosecution-relationships.md",
            "docs/recipes/cac-federal-trial-proceedings.md",
            "docs/recipes/cac-legal-sentencing-outcomes.md",
            "docs/recipes/cac-trafficking-recruitment-network.md",
        ),
    ),
    CACDomainFamily(
        domain_id="missing-child-investigation",
        title="Missing Child Investigations",
        keywords=(
            "missing child", "amber alert", "abduction", "stranger abduction",
            "runaway", "locate missing", "missing person", "child disappearance",
            "endangered missing", "recovery of missing",
        ),
        recipe_file="docs/recipes/cac-missing-child-investigation.md",
        mapping_source=None,
        layer=3,
        related_core_recipes=("docs/recipes/cell-site.md", "docs/recipes/location.md"),
    ),
    CACDomainFamily(
        domain_id="international-coordination",
        title="International Coordination and Cross-Border Operations",
        keywords=(
            "international", "cross-border", "europol", "interpol", "extradition",
            "foreign jurisdiction", "global operation", "transnational",
            "overseas", "philippines", "dark web agent",
        ),
        recipe_file="docs/recipes/cac-international-coordination.md",
        mapping_source="multi-jurisdictional rescue or task force operation",
        layer=3,
        related_core_recipes=("docs/recipes/cac-multi-jurisdiction-task-force.md",),
    ),
    CACDomainFamily(
        domain_id="production-case",
        title="CSAM Production and Manufacturing Cases",
        keywords=(
            "production", "manufacturing", "produced image", "produced video",
            "studio setup", "camera equipment", "offender-produced", "hands-on",
            "contact offense", "hands-on abuse",
            "csam production", "production of csam", "mobile recording device",
            "smartphone", "galaxy", "recording equipment",
        ),
        recipe_file="docs/recipes/cac-production-case.md",
        mapping_source=None,
        layer=2,
        related_core_recipes=(
            "docs/recipes/cac-csam-forensic-provenance.md",
            "docs/recipes/cac-federal-prosecution-relationships.md",
            "docs/recipes/exif-data.md",
        ),
    ),
)

GENERIC_CAC_KEYWORDS = (
    "crimes against children", "cac ontology", "child exploitation",
    "child victim", "icac", "internet crimes against children",
    "child abuse", "juvenile victim", "online exploitation",
)

PDF_NOISE_MARKERS = (
    "= menu", "eyeonannapolis.net", "https://www.", "buy tickets",
    "subscribe", "powered by", "latest posts", "advertisement",
    "you might be interested",
)

CAC_SIGNAL_MARKERS = (
    "icac", "child", "minor", "arrest", "charged", "solicitation",
    "trafficking", "cybertip", "ncmec", "search warrant", "csam",
    "exploitation", "task force", "rescue", "grooming",
    "co-conspirator", "enterprise", "indictment", "federal charge",
    "multi-district", "parallel jurisdiction", "forfeiture", "possession of csam",
)


def assess_extraction_quality(text: str) -> dict[str, Any]:
    """Detect noisy PDF/web extraction that lowers domain routing scores."""

    normalized = _normalize_text(text)
    noise_hits = sum(1 for marker in PDF_NOISE_MARKERS if marker in normalized)
    signal_hits = sum(1 for marker in CAC_SIGNAL_MARKERS if marker in normalized)
    url_count = normalized.count("https://")
    word_count = len(normalized.split())
    noisy = (
        url_count >= 5
        or (noise_hits >= 3 and signal_hits < 4)
        or (word_count > 4000 and signal_hits < 6)
    )
    payload: dict[str, Any] = {
        "noisy_extraction": noisy,
        "noise_marker_hits": noise_hits,
        "cac_signal_hits": signal_hits,
        "url_count": url_count,
        "word_count": word_count,
    }
    if noisy:
        payload["recommendation"] = (
            "PDF or web-page extraction appears noisy (ads, navigation, repeated URLs). "
            "For better recipe routing, pass a clean narrative excerpt via content_text "
            "after process_document_file, or summarize the investigative facts before calling "
            "route_cac_content."
        )
    return payload


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def score_domain_family(text: str, family: CACDomainFamily) -> int:
    """Score how well normalized text matches a CAC domain family."""

    normalized = _normalize_text(text)
    score = 0
    for keyword in family.keywords:
        if keyword in normalized:
            score += 1
    return score


def detect_cac_domains(text: str) -> list[dict[str, Any]]:
    """Return all CAC domain families scoring at or above the threshold."""

    normalized = _normalize_text(text)
    matches: list[dict[str, Any]] = []
    for family in CAC_DOMAIN_FAMILIES:
        score = score_domain_family(normalized, family)
        if score >= MIN_DOMAIN_SCORE:
            matches.append({
                "domain_id": family.domain_id,
                "title": family.title,
                "score": score,
                "layer": family.layer,
                "recipe_file": family.recipe_file,
                "mapping_source": family.mapping_source,
                "related_core_recipes": list(family.related_core_recipes),
            })
    matches.sort(key=lambda item: (-item["score"], item["layer"], item["domain_id"]))
    return matches


def cac_content_detected(text: str) -> bool:
    """Return True when text contains generic CAC signals or domain matches."""

    normalized = _normalize_text(text)
    if any(marker in normalized for marker in GENERIC_CAC_KEYWORDS):
        return True
    return any(score_domain_family(normalized, family) >= MIN_DOMAIN_SCORE for family in CAC_DOMAIN_FAMILIES)


def classify_input_path(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in GRAPH_EXTENSIONS:
        return "graph"
    if suffix in DOCUMENT_EXTENSIONS:
        return "document"
    return "unknown"


def extract_text_from_graph_file(path: Path) -> str:
    """Extract searchable text from a JSON-LD or Turtle graph file."""

    raw = path.read_text(encoding="utf-8", errors="replace")
    fragments: list[str] = [raw[:200_000]]

    if path.suffix.lower() in {".json", ".jsonld", ".json-ld"}:
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            return " ".join(fragments)
        graph = payload.get("@graph", payload if isinstance(payload, list) else [payload])
        if not isinstance(graph, list):
            graph = [graph]
        for node in graph:
            if not isinstance(node, dict):
                continue
            for key in ("uco-core:name", "uco-core:description", "rdfs:label", "rdfs:comment", "@type"):
                value = node.get(key)
                if isinstance(value, str):
                    fragments.append(value)
                elif isinstance(value, list):
                    fragments.extend(str(item) for item in value if isinstance(item, str))
    else:
        for match in re.finditer(
            r'(?:uco-core:name|rdfs:label|rdfs:comment|uco-core:description)\s+"([^"]{3,200})"',
            raw,
        ):
            fragments.append(match.group(1))

    return " ".join(fragments)


def graph_contains_cac_signals(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace").lower()
    return any(marker in raw for marker in CAC_IRI_MARKERS)


def _find_recipe_entry(recipe_file: str) -> dict[str, str] | None:
    for recipe in RECIPE_INDEX:
        if recipe["file"] == recipe_file:
            return recipe
    return None


def _find_mapping_guide(source: str | None) -> dict[str, Any] | None:
    if not source:
        return None
    source_lower = source.lower()
    for entry in MAPPING_GUIDE_INDEX:
        if entry["source"].lower() == source_lower:
            return {
                "source": entry["source"],
                "pattern": entry["pattern"],
                "classes": entry["classes"],
                "anti_patterns": entry["anti_patterns"],
                "code_skeleton": entry["code_skeleton"],
            }
    return None


def _load_recipe_content(project_root: Path, recipe_file: str, include_content: bool) -> dict[str, Any]:
    entry = _find_recipe_entry(recipe_file)
    title = entry["title"] if entry else recipe_file
    description = entry.get("description", "") if entry else ""
    payload: dict[str, Any] = {
        "title": title,
        "description": description,
        "file": recipe_file,
        "content": None,
        "truncated": False,
    }
    if not include_content:
        return payload
    try:
        content = (project_root / recipe_file).read_text(encoding="utf-8")
    except OSError:
        return payload
    payload["content"] = content[:MAX_RECIPE_CONTENT_CHARS]
    payload["truncated"] = len(content) > MAX_RECIPE_CONTENT_CHARS
    return payload


def build_validation_guidance(project_root: Path, output_format: str) -> dict[str, Any]:
    output_suffix = "jsonld" if output_format in {"jsonld", "json-ld", "json"} else "ttl"
    sample_output = f"output.{output_suffix}"
    import extension_paths

    subset_path = extension_paths.extension_dir("cac", project_root) / "validation-subset.json"
    return {
        "built_version": "case-1.4.0",
        "extension": "cac",
        "validation_mode": "subset",
        "subset_manifest": str(subset_path.relative_to(project_root)),
        "allow_info": True,
        "make_command": f"make validate-extension EXT=cac DATA={sample_output}",
        "mcp_tool": "validate_graph(graph_path, extensions=['cac'])",
        "full_manifest_tool": "validate_graph(graph_path, extensions=['cac:full'])",
        "output_formats": {
            "jsonld": "graph.write('output.jsonld') via CASEGraph (default SDK path)",
            "ttl": "graph.write('output.ttl', format='turtle') or serialize with rdflib after graph.write",
        },
        "note": (
            "MCP validate_graph uses the CAC validation-subset.json by default. "
            "Pass extensions=['cac:full'] for the complete CAC manifest when upstream "
            "SHACL SPARQL constraints are repaired."
        ),
    }


def build_modeling_checklist(matched_domains: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return prioritized completeness checks for connected CAC investigative graphs."""

    domain_ids = {item["domain_id"] for item in matched_domains}
    checks: list[dict[str, Any]] = [
        {
            "id": "perpetrator-crime-links",
            "priority": "critical",
            "check": (
                "Link the suspect/defendant as uco-action:performer on OnlineGrooming and "
                "procurement events (cacontology-physical:OnlinePurchase). Do not leave "
                "criminal-activity nodes isolated with only targetsVictim or a name."
            ),
            "recipes": [
                "docs/recipes/cac-grooming-chat-modeling.md",
                "docs/recipes/cac-csam-forensic-provenance.md",
            ],
        },
        {
            "id": "investigation-activity-scope",
            "priority": "critical",
            "check": (
                "Connect CACInvestigation to grooming/procurement scope via cacontology:hasStep "
                "(investigative actions) and an evidence-development InvestigativeAction that "
                "references exploitation event IRIs in uco-core:description. Use "
                "uco-core:Relationship kindOfRelationship='Concerns' only when both endpoints are "
                "uco-core:UcoObject (SHACL). Keep uco-core:object on Investigation limited to "
                "ObservableObject evidence (e.g., source PDF)."
            ),
            "recipes": ["docs/recipes/cac-icac-search-warrant-arrest.md"],
        },
        {
            "id": "phase-action-membership",
            "priority": "high",
            "check": (
                "Populate investigation phases (cacontology:InitialPhase, LegalProcessPhase, "
                "ConclusionPhase) with temporal bounds where known, cacontology:transitionsTo "
                "between phases, and cacontology:occursDuringPhase on InvestigativeActions. "
                "Remove or avoid empty phase shells."
            ),
            "recipes": ["docs/recipes/cac-icac-search-warrant-arrest.md"],
        },
        {
            "id": "agency-performer-dedup",
            "priority": "high",
            "check": (
                "Use one Organization node per agency (e.g., MSP CCU) with UcoObject typing for "
                "performer constraints. CAC SHACL allows one uco-action:performer per "
                "InvestigativeAction — document joint ICAC/county participation in descriptions "
                "or partnersWith when multiple agencies co-execute."
            ),
            "recipes": [
                "docs/recipes/cac-multi-jurisdiction-task-force.md",
                "docs/recipes/cac-icac-search-warrant-arrest.md",
            ],
        },
        {
            "id": "charge-offense-links",
            "priority": "medium",
            "check": (
                "Link charge nodes to underlying exploitation events via charge "
                "uco-core:description IRI references, or uco-core:Relationship (Relates_To) when "
                "both endpoints are UcoObject. Always keep chargedWith on every defendant Person — "
                "not only the principal suspect."
            ),
            "recipes": [
                "docs/recipes/cac-legal-sentencing-outcomes.md",
                "docs/recipes/cac-federal-prosecution-relationships.md",
            ],
        },
        {
            "id": "subject-location",
            "priority": "medium",
            "check": (
                "When a residence or search location is known, reference it on the suspect "
                "uco-core:description and on the warrant action uco-action:location. Use "
                "uco-core:Relationship Located_At only when the source endpoint is UcoObject."
            ),
            "recipes": ["docs/recipes/cac-icac-search-warrant-arrest.md"],
        },
        {
            "id": "provenance-source-chain",
            "priority": "medium",
            "check": (
                "Attach ProvenanceRecord with case-investigation:wasInformedBy to the source "
                "ObservableObject and authoring Tool. Preserve FileFacet + ContentDataFacet "
                "hashes on press-release PDFs."
            ),
            "recipes": ["docs/recipes/forensic-lifecycle.md"],
        },
    ]
    if "tactical-undercover" in domain_ids:
        checks.append({
            "id": "tactical-vs-routine-arrest",
            "priority": "high",
            "check": (
                "Use ArrestOperation with arrestType=warrant_arrest when custody was without "
                "incident; reserve HighRiskArrest/DynamicEntry for SWAT or resistance narratives."
            ),
            "recipes": ["docs/recipes/cac-tactical-undercover-operation.md"],
        })
    if "federal-prosecution-relationships" in domain_ids:
        checks.extend([
            {
                "id": "defendant-charge-matrix",
                "priority": "critical",
                "check": (
                    "For each defendant Person, add cacontology-legal-outcomes:chargedWith edges "
                    "to the specific FederalCharge nodes that defendant faces. Do not leave "
                    "numbered counts as orphan nodes. Use a DEFENDANT_COUNTS fact table when "
                    "the source assigns different counts to different defendants — subsets "
                    "often vary per count in multi-defendant indictments."
                ),
                "recipes": ["docs/recipes/cac-federal-prosecution-relationships.md"],
            },
            {
                "id": "indictment-charge-links",
                "priority": "critical",
                "check": (
                    "Link the charging instrument (indictment/complaint) to each FederalCharge via "
                    "uco-core:Relationship (Relates_To). Set indictmentCounts on the instrument and "
                    "chargeCount on each charge node."
                ),
                "recipes": ["docs/recipes/cac-federal-prosecution-relationships.md"],
            },
            {
                "id": "prosecution-indictment-link",
                "priority": "high",
                "check": (
                    "Connect FederalProsecution to the charging instrument via "
                    "uco-core:Relationship (Relates_To). Add a FederalProsecution per lead "
                    "district when parallel dockets exist."
                ),
                "recipes": ["docs/recipes/cac-federal-prosecution-relationships.md"],
            },
            {
                "id": "investigation-legal-scope",
                "priority": "high",
                "check": (
                    "Link CACInvestigation to indictment, prosecution, charges, and/or CSAMIncident "
                    "via uco-core:Relationship (Relates_To) or case-investigation:object. "
                    "case-investigation:focus text supplements but does not replace graph edges."
                ),
                "recipes": ["docs/recipes/cac-federal-prosecution-relationships.md"],
            },
            {
                "id": "multi-district-charge-jurisdiction",
                "priority": "high",
                "check": (
                    "When charges span multiple federal districts, link each district-prefixed "
                    "FederalCharge to its court Location and add parallel_jurisdiction from "
                    "CACInvestigation to each non-primary district."
                ),
                "recipes": ["docs/recipes/cac-federal-prosecution-relationships.md"],
            },
            {
                "id": "forfeiture-device-linkage",
                "priority": "high",
                "check": (
                    "When forfeiture enumerates specific devices, set targetedAsset on "
                    "AssetForfeitureAction to each MobileRecordingDevice — not only a generic "
                    "aggregate stub. Add relatedCriminalCharges linking forfeiture to "
                    "supporting FederalCharge nodes."
                ),
                "recipes": [
                    "docs/recipes/cac-federal-prosecution-relationships.md",
                    "docs/recipes/cac-production-case.md",
                ],
            },
            {
                "id": "enterprise-indictment-bridge",
                "priority": "high",
                "check": (
                    "When ChildExploitationEnterprise is alleged, connect it to the charging "
                    "instrument via Relates_To and/or cacontology:resultsInIndictment from "
                    "ConspiracyToCommitCSA. Complete gufo:hasParticipant on all Relators."
                ),
                "recipes": ["docs/recipes/cac-federal-prosecution-relationships.md"],
            },
            {
                "id": "enterprise-overt-act-violations",
                "priority": "high",
                "check": (
                    "When Count 1 (§ 2252A(g)) embeds Violation One/Two/… paragraphs, model "
                    "each violation as a conduct node with Relates_To from the enterprise "
                    "charge, per-violation venue Location, and defendant subsets via "
                    "participatesInEvent — do not flatten Count 1 into a single node."
                ),
                "recipes": ["docs/recipes/cac-federal-prosecution-relationships.md"],
            },
            {
                "id": "charge-venue-locations",
                "priority": "high",
                "check": (
                    "When counts or violations name judicial districts (e.g., D. New Mexico, "
                    "S.D. California), link each FederalCharge or overt-act node to that "
                    "venue Location via Relates_To — not only the filing court."
                ),
                "recipes": ["docs/recipes/cac-federal-prosecution-relationships.md"],
            },
            {
                "id": "transnational-extradition-chain",
                "priority": "high",
                "check": (
                    "When the defendant is abroad or extradition is alleged, link "
                    "ExtraditionProcess to the defendant Person and FederalProsecution via "
                    "Relates_To. Model foreign residence as InternationalJurisdiction or "
                    "Location."
                ),
                "recipes": [
                    "docs/recipes/cac-federal-prosecution-relationships.md",
                    "docs/recipes/cac-international-coordination.md",
                ],
            },
            {
                "id": "financial-charge-stacking",
                "priority": "high",
                "check": (
                    "When indictments stack wire fraud (§ 1343), aggravated identity theft "
                    "(§ 1028A), or cyberstalking (§ 2261A) on CSEA counts, link each "
                    "non-CSEA FederalCharge to SextortionScheme, CSAMIncident, or "
                    "impersonation conduct via Relates_To."
                ),
                "recipes": [
                    "docs/recipes/cac-federal-prosecution-relationships.md",
                    "docs/recipes/cac-sextortion-coercion.md",
                ],
            },
        ])
    if "sextortion-coercion" in domain_ids:
        checks.extend([
            {
                "id": "sextortion-federal-prosecution-bridge",
                "priority": "critical",
                "check": (
                    "When the source is a sextortion indictment, wire SextortionScheme to "
                    "FederalCharge nodes (cyberstalking, wire fraud, identity theft) and add "
                    "chargedWith on the defendant. Run the federal prosecution relationship "
                    "checklist for indictment, prosecution, and forfeiture edges."
                ),
                "recipes": [
                    "docs/recipes/cac-sextortion-coercion.md",
                    "docs/recipes/cac-federal-prosecution-relationships.md",
                ],
            },
            {
                "id": "platform-affordance-abuse",
                "priority": "medium",
                "check": (
                    "Link used_platform from SextortionScheme or enterprise to Instagram, "
                    "Snapchat, Dropbox, or other platforms named in the indictment. Record "
                    "ban-evasion and account-recreation counts in uco-core:description when "
                    "alleged — do not bury platform affordance detail only in Bundle text."
                ),
                "recipes": ["docs/recipes/cac-sextortion-coercion.md"],
            },
        ])
    if "trafficking-recruitment" in domain_ids:
        checks.extend([
            {
                "id": "per-victim-charge-bundles",
                "priority": "critical",
                "check": (
                    "When indictments assign counts per Minor Victim 1–N, use a VICTIM_COUNTS "
                    "fact table and Relates_To from each FederalCharge to the victim role and "
                    "conduct node (CommercialSexualExploitation, CSAMIncident, enticement). "
                    "Do not use TraffickingRing for solo-operator § 1591 cases."
                ),
                "recipes": [
                    "docs/recipes/cac-trafficking-recruitment-network.md",
                    "docs/recipes/cac-federal-prosecution-relationships.md",
                ],
            },
            {
                "id": "trafficking-conduct-charge-bridge",
                "priority": "high",
                "check": (
                    "Link § 1591 FederalCharge nodes to CommercialSexualExploitation conduct "
                    "and DigitalToPhysicalBridge (Grindr/messaging → in-person). Model "
                    "VictimTransportation when rideshare/taxi/hotel transport is alleged."
                ),
                "recipes": ["docs/recipes/cac-trafficking-recruitment-network.md"],
            },
            {
                "id": "stacked-statute-per-encounter",
                "priority": "high",
                "check": (
                    "When one encounter supports production (§ 2251), trafficking (§ 1591), "
                    "enticement (§ 2422), and distribution/receipt (§ 2252), link all applicable "
                    "FederalCharge nodes to the same exploitation conduct node — not isolated charges."
                ),
                "recipes": [
                    "docs/recipes/cac-trafficking-recruitment-network.md",
                    "docs/recipes/cac-production-case.md",
                ],
            },
        ])
    if "federal-trial-proceedings" in domain_ids:
        checks.extend([
            {
                "id": "superseding-indictment-chain",
                "priority": "critical",
                "check": (
                    "Link original indictment to superseding instrument via supersededBy or "
                    "Relates_To. Point FederalProsecution at the current superseding indictment. "
                    "Record filing dates and ECF document numbers."
                ),
                "recipes": [
                    "docs/recipes/cac-federal-trial-proceedings.md",
                    "docs/recipes/cac-federal-prosecution-relationships.md",
                ],
            },
            {
                "id": "trial-brief-anticipated-evidence",
                "priority": "high",
                "check": (
                    "When a government trial brief describes per-victim anticipated testimony "
                    "and exhibits, link brief sections to victim roles, FederalCharge nodes, "
                    "and ObservableObject exhibit devices (e.g., 1B10). Mark as ALLEGED."
                ),
                "recipes": [
                    "docs/recipes/cac-federal-trial-proceedings.md",
                    "docs/recipes/cac-csam-forensic-provenance.md",
                ],
            },
            {
                "id": "docket-procedural-milestones",
                "priority": "medium",
                "check": (
                    "Extract competency hearings, detention orders, Speedy Trial Act exclusions, "
                    "and trial date settings as dated InvestigativeAction or Event nodes — not "
                    "only unstructured docket text on the Bundle."
                ),
                "recipes": ["docs/recipes/cac-federal-trial-proceedings.md"],
            },
        ])
    if "pacer-document-ingestion" in domain_ids:
        checks.extend([
            {
                "id": "pacer-single-investigation-per-docket",
                "priority": "critical",
                "check": (
                    "Build one CACInvestigation per federal docket number, not one graph per "
                    "PDF. Link each source PDF as uco-core:object on the investigation and "
                    "attach a ProvenanceRecord with case-investigation:wasInformedBy."
                ),
                "recipes": ["docs/recipes/cac-pacer-document-ingestion.md"],
            },
            {
                "id": "pacer-no-fabricated-timestamps",
                "priority": "critical",
                "check": (
                    "Only assert startTime/dateTime values the source document actually "
                    "states. When a filing gives month precision only ('June 2019', "
                    "'January and February 2020'), record the period in the description or "
                    "an approximatePeriod facet string — never invent a day or clock time. "
                    "Use uco-action:startTime only on Action subclasses; use "
                    "uco-core:startTime on Events, phases, and observables."
                ),
                "recipes": ["docs/recipes/cac-pacer-document-ingestion.md"],
            },
            {
                "id": "pacer-judgment-supervision-conditions",
                "priority": "high",
                "check": (
                    "From AO 245B judgments, model SupervisedRelease plus each Sheet 3D "
                    "special condition as its own node linked via Requires, and model "
                    "restitution, special assessment, and the Sheet 6 payment schedule as "
                    "separate MonetaryPenalty / schedule nodes."
                ),
                "recipes": [
                    "docs/recipes/cac-pacer-document-ingestion.md",
                    "docs/recipes/cac-legal-sentencing-outcomes.md",
                ],
            },
            {
                "id": "pacer-assertion-status-tags",
                "priority": "high",
                "check": (
                    "Tag pre-adjudication conduct assertion:ALLEGED and post-verdict "
                    "outcomes assertion:ADJUDICATED. Keep page-anchored source references "
                    "(Source: PACER Doc N, page X) in every description."
                ),
                "recipes": ["docs/recipes/cac-pacer-document-ingestion.md"],
            },
        ])
    if "production-case" in domain_ids and "federal-prosecution-relationships" not in domain_ids:
        checks.append({
            "id": "production-equipment-conduct",
            "priority": "high",
            "check": (
                "Link CSAMIncident or production offense nodes to MobileRecordingDevice via "
                "used_equipment Relationship or cacontology-production:usesEquipment. When "
                "forfeiture is alleged, bridge the same devices through targetedAsset."
            ),
            "recipes": ["docs/recipes/cac-production-case.md"],
        })
    return checks


def build_workflow_steps(matched_domains: list[dict[str, Any]], output_format: str) -> list[str]:
    layers_present = sorted({item["layer"] for item in matched_domains})
    steps = [
        "Set CASE_UCO_EXTENSIONS=cac in the MCP server and SDK environment.",
        f"Target output format: {output_format} (JSON-LD for Link-Look/Hermes default; TTL when requested).",
    ]
    if 1 in layers_present:
        steps.append(
            "Layer 1 — Model observable evidence first (messages, images, devices, hashes) "
            "using core CASE/UCO types plus CAC forensic classes where applicable."
        )
    if 2 in layers_present:
        steps.append(
            "Layer 2 — Add CAC behavioral interpretation (grooming, trafficking, sextortion, "
            "production) without collapsing evidence and interpretation into one node."
        )
    if 3 in layers_present:
        steps.append(
            "Layer 3 — Model institutional workflow (CyberTips, task force ops, rescue, "
            "sentencing) and link layers with explicit CASE/UCO properties."
        )
    steps.extend([
        (
            "Follow each matched recipe below; compose into one investigation graph unless "
            "natural forensic boundaries require separate graphs."
        ),
        (
            "Review modeling_checklist before finalize — connect suspect→crime, investigation→activities, "
            "phases→actions, defendant→counts, enterprise→indictment, and charges→offenses."
        ),
        "Call validate_graph with extensions=['cac'] on the finished graph.",
        "Link-Look users may perform additional visual validation in Normalize view.",
    ])
    return steps


def resolve_submission_text(
    content_text: str | None,
    source_path: str | None,
    project_root: Path,
) -> tuple[str, str, dict[str, Any]]:
    """Resolve analyzable text and classify the submission input type."""

    metadata: dict[str, Any] = {}
    if source_path:
        path = Path(source_path).expanduser()
        if not path.is_absolute():
            path = (project_root / path).resolve()
        else:
            path = path.resolve()
        metadata["source_path"] = str(path)
        if not path.exists():
            raise ValueError("source_missing")

        input_kind = classify_input_path(path)
        if input_kind == "graph":
            text = extract_text_from_graph_file(path)
            metadata["graph_has_cac_signals"] = graph_contains_cac_signals(path)
            if content_text:
                text = f"{content_text}\n{text}"
            if metadata["graph_has_cac_signals"]:
                return text, "graph_partial", metadata
            return text, "graph_core_only", metadata

        if input_kind == "document":
            if path.suffix.lower() in {".txt", ".md", ".csv", ".tsv"}:
                text = path.read_text(encoding="utf-8", errors="replace")
                if content_text:
                    text = f"{content_text}\n{text}"
                return text, "structured_text" if path.suffix.lower() in {".csv", ".tsv"} else "free_text", metadata
            metadata["document_processing_note"] = (
                "Binary or office documents should be processed with process_document_file "
                "first; pass extracted text back via content_text for CAC recipe routing."
            )
            if content_text:
                return content_text, "file_reference", metadata
            raise ValueError("document_requires_extraction")

        if content_text:
            return content_text, "free_text", metadata
        raise ValueError("unsupported_source_type")

    if content_text:
        return content_text, "free_text", metadata
    raise ValueError("empty_submission")


def route_cac_content(
    project_root: Path,
    content_text: str | None = None,
    source_path: str | None = None,
    output_format: str = "jsonld",
    include_recipe_content: bool = True,
    max_recipes: int = 6,
) -> dict[str, Any]:
    """Route a submission to one or more CAC recipes and validation guidance."""

    normalized_format = output_format.lower().replace("_", "-")
    if normalized_format not in {"jsonld", "json-ld", "json", "ttl", "turtle"}:
        raise ValueError("unsupported_output_format")

    text, input_type, input_metadata = resolve_submission_text(
        content_text=content_text,
        source_path=source_path,
        project_root=project_root,
    )

    extraction_quality = assess_extraction_quality(text)
    if extraction_quality.get("noisy_extraction"):
        input_metadata["extraction_quality"] = extraction_quality

    generic_hit = any(kw in _normalize_text(text) for kw in GENERIC_CAC_KEYWORDS)
    matched_domains = detect_cac_domains(text)
    cac_detected = generic_hit or bool(matched_domains) or bool(
        input_metadata.get("graph_has_cac_signals")
    )

    if not cac_detected:
        return {
            "ok": True,
            "cac_detected": False,
            "content_trust": "untrusted-source-content",
            "input_type": input_type,
            "output_format": "json-ld" if normalized_format in {"jsonld", "json-ld", "json"} else "ttl",
            "matched_domains": [],
            "message": (
                "No CAC Ontology domain patterns detected. Call "
                "route_investigation_content for general investigation-type "
                "routing (violent crime, financial crime, court filings, "
                "network intrusion, device forensics, ...), or use "
                "find_classes_for_domain / guide_mapping for core CASE/UCO "
                "workflows."
            ),
            **input_metadata,
        }

    if not matched_domains and generic_hit:
        matched_domains = [{
            "domain_id": "cac-general",
            "title": "CAC General Investigation (cross-ontology-composition)",
            "score": 1,
            "layer": 2,
            "recipe_file": "docs/recipes/cross-ontology-composition.md",
            "mapping_source": None,
            "related_core_recipes": ["docs/recipes/cac-grooming-chat-modeling.md"],
        }]

    trimmed = matched_domains[: max(1, max_recipes)]
    enriched: list[dict[str, Any]] = []
    for domain in trimmed:
        enriched.append({
            **domain,
            "recipe": _load_recipe_content(
                project_root,
                domain["recipe_file"],
                include_recipe_content,
            ),
            "mapping_guide": _find_mapping_guide(domain.get("mapping_source")),
        })

    return {
        "ok": True,
        "cac_detected": True,
        # Submitted content is evidence, not instructions (see SECURITY.md).
        "content_trust": "untrusted-source-content",
        "input_type": input_type,
        "output_format": "json-ld" if normalized_format in {"jsonld", "json-ld", "json"} else "ttl",
        "matched_domains": enriched,
        "extraction_quality": extraction_quality,
        "recommended_workflow": build_workflow_steps(trimmed, normalized_format),
        "modeling_checklist": build_modeling_checklist(trimmed),
        "validation": build_validation_guidance(project_root, normalized_format),
        "integration_note": (
            "Hermes and Link-Look share this MCP server. Return JSON-LD for default "
            "SDK serialization; request TTL when the downstream tool consumes Turtle."
        ),
        **input_metadata,
    }


def search_recipes(scenario: str, limit: int = 5, include_content: bool = False) -> list[dict[str, Any]]:
    """Return multiple recipe matches for a scenario query (not just the best one)."""

    q = scenario.lower()
    scored: list[tuple[int, dict[str, str]]] = []
    for recipe in RECIPE_INDEX:
        text = f"{recipe['title']} {recipe['description']} {recipe['keywords']}".lower()
        score = sum(1 for word in q.split() if word and word in text)
        if "cac" in q or "child" in q or "trafficking" in q or "grooming" in q or "icac" in q:
            if "cac" in text or "child" in text or "grooming" in text or "cybertip" in text:
                score += 1
        if score > 0:
            scored.append((score, recipe))
    scored.sort(key=lambda item: (-item[0], item[1]["title"]))
    results: list[dict[str, Any]] = []
    project_root = Path(__file__).resolve().parent.parent
    for score, recipe in scored[:limit]:
        payload = {
            "score": score,
            "title": recipe["title"],
            "description": recipe["description"],
            "file": recipe["file"],
        }
        if include_content:
            try:
                content = (project_root / recipe["file"]).read_text(encoding="utf-8")
                payload["content"] = content[:MAX_RECIPE_CONTENT_CHARS]
                payload["truncated"] = len(content) > MAX_RECIPE_CONTENT_CHARS
            except OSError:
                payload["content"] = None
                payload["truncated"] = False
        results.append(payload)
    return results
