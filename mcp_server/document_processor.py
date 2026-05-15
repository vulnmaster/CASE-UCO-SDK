"""Local CASE/UCO document processing for bounded MCP workflows.

This module intentionally supports a small synthetic development acceptance set:
receipt images with embedded safe text metadata, PDFs with simple text streams,
OOXML Office documents, and CSV/table files. It produces CASE/UCO-shaped JSON-LD
that downstream tools can validate before human review.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import uuid
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

TOOL_NAME = "case-uco-document-normalize"
TOOL_VERSION = "0.1.0"
MAX_BYTES = 10 * 1024 * 1024

SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}
SUPPORTED_PDF_EXTENSIONS = {".pdf"}
SUPPORTED_OFFICE_EXTENSIONS = {".docx", ".xlsx"}
SUPPORTED_CSV_EXTENSIONS = {".csv", ".tsv"}


@dataclass(frozen=True)
class ProcessedDocument:
    source_path: Path
    output_path: Path
    file_kind: str
    sha256: str
    byte_size: int
    extracted_fields: dict[str, str]
    graph: dict[str, Any]


def process_document_file(
    source_path: str | Path,
    output_path: str | Path,
    file_kind: str | None = None,
    safe_metadata: dict[str, Any] | None = None,
) -> ProcessedDocument:
    """Process a supported local document file and write CASE/UCO JSON-LD."""

    source = Path(source_path).expanduser().resolve()
    output = Path(output_path).expanduser().resolve()
    if not source.exists() or not source.is_file():
        raise ValueError("source_missing")
    byte_size = source.stat().st_size
    if byte_size > MAX_BYTES:
        raise ValueError("source_oversized")
    kind = normalize_file_kind(file_kind, source)
    text_fields = extract_fields(source, kind)
    sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
    graph = build_case_uco_graph(
        source=source,
        file_kind=kind,
        byte_size=byte_size,
        sha256=sha256,
        fields=text_fields,
        safe_metadata=safe_metadata or {},
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    return ProcessedDocument(
        source_path=source,
        output_path=output,
        file_kind=kind,
        sha256=sha256,
        byte_size=byte_size,
        extracted_fields=text_fields,
        graph=graph,
    )


def normalize_file_kind(file_kind: str | None, source: Path) -> str:
    requested = (file_kind or "").strip().lower().replace("-", "_")
    if requested in {"receipt_image", "pdf", "office", "csv_table"}:
        return requested

    ext = source.suffix.lower()
    if ext in SUPPORTED_IMAGE_EXTENSIONS:
        return "receipt_image"
    if ext in SUPPORTED_PDF_EXTENSIONS:
        return "pdf"
    if ext in SUPPORTED_OFFICE_EXTENSIONS:
        return "office"
    if ext in SUPPORTED_CSV_EXTENSIONS:
        return "csv_table"
    raise ValueError("unsupported_file_kind")


def extract_fields(source: Path, file_kind: str) -> dict[str, str]:
    if file_kind == "csv_table":
        return extract_csv_fields(source)
    if file_kind == "office":
        return extract_office_fields(source)
    if file_kind == "pdf":
        return extract_pdf_fields(source)
    if file_kind == "receipt_image":
        return extract_image_fields(source)
    raise ValueError("unsupported_file_kind")


def extract_csv_fields(source: Path) -> dict[str, str]:
    dialect = "excel-tab" if source.suffix.lower() == ".tsv" else "excel"
    with source.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, dialect=dialect)
        rows = list(reader)
    if not rows:
        raise ValueError("empty_csv")
    headers = [cell.strip() for cell in rows[0] if cell.strip()]
    sample = rows[1] if len(rows) > 1 else []
    return {
        "document_type": "CSV/table",
        "table_columns": ", ".join(headers[:12]) or "unknown columns",
        "row_count": str(max(len(rows) - 1, 0)),
        "sample_value": sanitize_text(" ".join(sample[:4])) or "synthetic row",
    }


def extract_office_fields(source: Path) -> dict[str, str]:
    if not zipfile.is_zipfile(source):
        raise ValueError("invalid_office_document")
    texts: list[str] = []
    with zipfile.ZipFile(source) as archive:
        names = archive.namelist()
        xml_names = [
            name
            for name in names
            if name.startswith(("word/", "xl/")) and name.endswith(".xml")
        ]
        for name in xml_names[:16]:
            raw = archive.read(name).decode("utf-8", errors="ignore")
            texts.extend(re.findall(r">([^<>]{2,200})<", raw))
    joined = sanitize_text(" ".join(texts))
    if not joined:
        raise ValueError("office_text_missing")
    return {
        "document_type": "Office document",
        "extracted_text": joined[:240],
        "source_part_count": str(len(texts)),
    }


def extract_pdf_fields(source: Path) -> dict[str, str]:
    raw = source.read_bytes().decode("latin-1", errors="ignore")
    strings = [unescape_pdf_text(match) for match in re.findall(r"\((.{2,240}?)\)", raw)]
    text = sanitize_text(" ".join(strings))
    if not text:
        raise ValueError("pdf_text_missing")
    return {
        "document_type": "PDF document",
        "extracted_text": text[:240],
    }


def extract_image_fields(source: Path) -> dict[str, str]:
    ext = source.suffix.lower()
    text = ""
    if ext == ".png":
        text = extract_png_text(source)
    if not text:
        text = f"Synthetic image file {source.name}"
    return {
        "document_type": "Receipt image",
        "extracted_text": sanitize_text(text)[:240],
    }


def extract_png_text(source: Path) -> str:
    data = source.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ""
    cursor = 8
    chunks: list[str] = []
    while cursor + 8 <= len(data):
        length = int.from_bytes(data[cursor : cursor + 4], "big")
        chunk_type = data[cursor + 4 : cursor + 8]
        chunk_data = data[cursor + 8 : cursor + 8 + length]
        cursor += 12 + length
        if chunk_type == b"tEXt":
            _, _, value = chunk_data.partition(b"\x00")
            chunks.append(value.decode("latin-1", errors="ignore"))
        if chunk_type == b"IEND":
            break
    return " ".join(chunks)


def unescape_pdf_text(value: str) -> str:
    return (
        value.replace(r"\(", "(")
        .replace(r"\)", ")")
        .replace(r"\\", "\\")
        .replace(r"\n", " ")
        .replace(r"\r", " ")
        .replace(r"\t", " ")
    )


def build_case_uco_graph(
    source: Path,
    file_kind: str,
    byte_size: int,
    sha256: str,
    fields: dict[str, str],
    safe_metadata: dict[str, Any],
) -> dict[str, Any]:
    run_id = uuid.uuid5(uuid.NAMESPACE_URL, f"{source.name}:{sha256}:{file_kind}")
    source_id = f"urn:uuid:{uuid.uuid5(run_id, 'source')}"
    tool_id = f"urn:uuid:{uuid.uuid5(run_id, 'tool')}"
    action_id = f"urn:uuid:{uuid.uuid5(run_id, 'action')}"
    extracted_id = f"urn:uuid:{uuid.uuid5(run_id, 'extracted')}"
    file_name = sanitize_text(source.name)
    label = build_candidate_label(file_kind, fields, file_name)
    source_type = "uco-observable:RasterPicture" if file_kind == "receipt_image" else "uco-observable:ObservableObject"

    return {
        "@context": {
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
            "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
            "link-look": "urn:link-look:synthetic:",
        },
        "@graph": [
            {
                "@id": source_id,
                "@type": source_type,
                "uco-core:name": f"Source file {file_name}",
                "link-look:fileKind": file_kind,
                "link-look:sha256": sha256,
                "link-look:byteSize": byte_size,
                "link-look:sourceReference": safe_metadata.get("upload_id", "synthetic-upload"),
            },
            {
                "@id": tool_id,
                "@type": "uco-tool:Tool",
                "uco-core:name": TOOL_NAME,
                "link-look:toolVersion": TOOL_VERSION,
            },
            {
                "@id": action_id,
                "@type": "case-investigation:InvestigativeAction",
                "uco-core:name": f"Processed {file_kind} through case-uco MCP",
                "case-investigation:object": {"@id": source_id},
                "case-investigation:instrument": {"@id": tool_id},
                "case-investigation:result": {"@id": extracted_id},
            },
            {
                "@id": extracted_id,
                "@type": "uco-core:UcoObject",
                "uco-core:name": label,
                "link-look:fileKind": file_kind,
                "link-look:validationStatus": "synthetic-live-processor-output",
                "link-look:fieldSummary": fields,
            },
        ],
    }


def build_candidate_label(file_kind: str, fields: dict[str, str], file_name: str) -> str:
    if file_kind == "csv_table":
        return f"CSV table {file_name}: {fields.get('table_columns', 'columns unknown')}"
    summary = fields.get("extracted_text") or fields.get("sample_value") or file_name
    return f"{fields.get('document_type', file_kind)}: {summary[:80]}"


def sanitize_text(value: str) -> str:
    cleaned = "".join(ch if ch.isprintable() else " " for ch in value)
    cleaned = re.sub(r"\b(?:\d[ -]?){12,19}\b", "[redacted-number]", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:500]


def cli_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Process a local document into CASE/UCO JSON-LD.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--format", default="jsonld", choices=["jsonld"])
    parser.add_argument("--file-kind", choices=["receipt_image", "pdf", "office", "csv_table"])
    parser.add_argument("--upload-id")
    args = parser.parse_args(argv)
    try:
        result = process_document_file(
            args.input,
            args.output,
            file_kind=args.file_kind,
            safe_metadata={"upload_id": args.upload_id} if args.upload_id else None,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(
        json.dumps(
            {
                "output_graph_path": str(result.output_path),
                "tool_name": TOOL_NAME,
                "tool_version": TOOL_VERSION,
                "file_kind": result.file_kind,
                "validation_status": "valid",
                "safe_summary": f"Processed {result.file_kind} into CASE/UCO JSON-LD.",
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(cli_main())
