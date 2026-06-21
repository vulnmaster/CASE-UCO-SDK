"""Tests for the canonical-term document processor (Tier T0 synthetic data)."""

import json
import struct
import sys
import zlib
import zipfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import document_processor


def write_png_with_text(path: Path, text: str) -> None:
    def chunk(kind: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(kind + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", crc)

    raw = b"\x00\xff\xff\xff"
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
        + chunk(b"tEXt", b"Receipt\x00" + text.encode("latin-1"))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


def write_plain_png(path: Path) -> None:
    """PNG with no tEXt chunk — no embedded text to extract."""

    def chunk(kind: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(kind + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", crc)

    raw = b"\x00\xff\xff\xff"
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


def write_pdf(path: Path) -> None:
    path.write_text(
        "%PDF-1.4\n1 0 obj <<>> stream\nBT (Synthetic PDF invoice total 23.45) Tj ET\nendstream\nendobj\n%%EOF\n",
        encoding="latin-1",
    )


def write_flate_pdf(path: Path) -> None:
    """PDF whose only text lives inside a Flate-compressed content stream."""

    content = zlib.compress(b"BT (Synthetic compressed-stream invoice total 99.10) Tj ET")
    path.write_bytes(
        b"%PDF-1.4\n1 0 obj << /Filter /FlateDecode >>\nstream\n"
        + content
        + b"\nendstream\nendobj\n%%EOF\n"
    )


def write_scanned_pdf(path: Path) -> None:
    """PDF with no extractable text strings (image-only / scanned shape)."""

    path.write_bytes(b"%PDF-1.4\n1 0 obj << /Subtype /Image >>\nstream\n\x00\x01\x02\nendstream\nendobj\n%%EOF\n")


def write_docx(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types></Types>")
        archive.writestr(
            "word/document.xml",
            "<w:document><w:body><w:p><w:r><w:t>Synthetic Office document item Alpha</w:t></w:r></w:p></w:body></w:document>",
        )


def write_xlsx(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types></Types>")
        archive.writestr(
            "xl/sharedStrings.xml",
            '<sst><si><t>Synthetic spreadsheet cell Bravo</t></si></sst>',
        )
        archive.writestr("xl/worksheets/sheet1.xml", "<worksheet><sheetData/></worksheet>")


def graph_nodes(output: Path) -> list[dict]:
    return json.loads(output.read_text(encoding="utf-8"))["@graph"]


def nodes_of_type(nodes: list[dict], type_name: str) -> list[dict]:
    return [node for node in nodes if node.get("@type") == type_name]


# ---------------------------------------------------------------------------
# Canonical graph shape (#102)
# ---------------------------------------------------------------------------


def test_graph_uses_canonical_action_provenance_terms(tmp_path: Path) -> None:
    source = tmp_path / "receipt.png"
    write_png_with_text(source, "Synthetic receipt total 12.34")
    output = tmp_path / "receipt.jsonld"
    document_processor.process_document_file(source, output, safe_metadata={"upload_id": "synthetic-upload-1"})

    raw = output.read_text(encoding="utf-8")
    # Invented predicates from v0.1.0 must be gone.
    assert "case-investigation:object" not in raw
    assert "case-investigation:instrument" not in raw
    assert "case-investigation:result" not in raw
    assert "link-look:" not in raw

    nodes = graph_nodes(output)
    actions = nodes_of_type(nodes, "case-investigation:InvestigativeAction")
    assert len(actions) == 1
    action = actions[0]
    assert action["uco-action:object"]["@id"]
    assert action["uco-action:instrument"]["@id"]
    assert action["uco-action:result"], "action must reference extracted records"
    assert action["uco-action:startTime"]["@type"] == "xsd:dateTime"


def test_source_node_carries_file_and_hash_facets(tmp_path: Path) -> None:
    source = tmp_path / "receipt.png"
    write_png_with_text(source, "Synthetic receipt total 12.34")
    output = tmp_path / "receipt.jsonld"
    result = document_processor.process_document_file(source, output)

    nodes = graph_nodes(output)
    sources = nodes_of_type(nodes, "uco-observable:RasterPicture")
    assert len(sources) == 1
    facets = sources[0]["uco-core:hasFacet"]
    file_facets = [f for f in facets if f["@type"] == "uco-observable:FileFacet"]
    content_facets = [f for f in facets if f["@type"] == "uco-observable:ContentDataFacet"]
    assert file_facets[0]["uco-observable:fileName"] == "receipt.png"
    assert file_facets[0]["uco-observable:extension"] == "png"
    hash_node = content_facets[0]["uco-observable:hash"][0]
    assert hash_node["@type"] == "uco-types:Hash"
    # Plain xsd:string per UCO 1.4.0+ guidance (typed vocab literal warns).
    assert hash_node["uco-types:hashMethod"] == "SHA256"
    assert hash_node["uco-types:hashValue"]["@value"] == result.sha256.upper()


def test_tool_node_uses_canonical_version_property(tmp_path: Path) -> None:
    source = tmp_path / "table.csv"
    source.write_text("item,total\nalpha,12.34\n", encoding="utf-8")
    output = tmp_path / "table.jsonld"
    document_processor.process_document_file(source, output)

    tools = nodes_of_type(graph_nodes(output), "uco-tool:Tool")
    assert len(tools) == 1
    assert tools[0]["uco-tool:version"] == document_processor.TOOL_VERSION


def test_records_carry_extracted_strings_facets_and_relationships(tmp_path: Path) -> None:
    source = tmp_path / "table.csv"
    source.write_text("item,total\nalpha,12.34\nbravo,56.78\n", encoding="utf-8")
    output = tmp_path / "table.jsonld"
    result = document_processor.process_document_file(source, output)

    assert len(result.records) == 2
    nodes = graph_nodes(output)
    observables = nodes_of_type(nodes, "uco-observable:ObservableObject")
    record_nodes = [n for n in observables if n.get("uco-core:hasFacet")
                    and any(f["@type"] == "uco-observable:ExtractedStringsFacet" for f in n["uco-core:hasFacet"])]
    assert len(record_nodes) == 2
    strings_facet = record_nodes[0]["uco-core:hasFacet"][0]
    assert strings_facet["uco-observable:strings"][0]["@type"] == "uco-observable:ExtractedString"
    assert "item=alpha" in strings_facet["uco-observable:strings"][0]["uco-observable:stringValue"]

    relationships = nodes_of_type(nodes, "uco-core:Relationship")
    assert len(relationships) == 2
    assert relationships[0]["uco-core:kindOfRelationship"] == "Derived_From"
    record_ids = {n["@id"] for n in record_nodes}
    assert relationships[0]["uco-core:source"]["@id"] in record_ids


# ---------------------------------------------------------------------------
# Extraction breadth and honest failure (#103)
# ---------------------------------------------------------------------------


def test_csv_yields_bounded_per_record_candidates(tmp_path: Path) -> None:
    rows = "\n".join(f"row-{i},{i}.00" for i in range(1, document_processor.MAX_CSV_RECORDS + 51))
    source = tmp_path / "big.csv"
    source.write_text("item,total\n" + rows + "\n", encoding="utf-8")
    output = tmp_path / "big.jsonld"
    result = document_processor.process_document_file(source, output)

    assert len(result.records) == document_processor.MAX_CSV_RECORDS
    assert result.truncated is True
    assert result.extracted_fields["truncated"].startswith(f"first {document_processor.MAX_CSV_RECORDS}")


def test_empty_csv_fails_honestly(tmp_path: Path) -> None:
    source = tmp_path / "empty.csv"
    source.write_text("item,total\n", encoding="utf-8")
    with pytest.raises(ValueError, match="empty_csv"):
        document_processor.process_document_file(source, tmp_path / "out.jsonld")


def test_flate_compressed_pdf_text_is_extracted(tmp_path: Path) -> None:
    source = tmp_path / "compressed.pdf"
    write_flate_pdf(source)
    output = tmp_path / "compressed.jsonld"
    result = document_processor.process_document_file(source, output)
    assert "compressed-stream invoice" in result.extracted_fields["extracted_text"]


def test_scanned_pdf_without_text_fails_honestly(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "scanned.pdf"
    write_scanned_pdf(source)
    # Force the no-extractor environment regardless of host tooling.
    monkeypatch.setattr(document_processor, "extract_pdf_text_pdftotext", lambda _s: "")
    monkeypatch.setattr(document_processor, "extract_pdf_text_pypdf", lambda _s: "")
    monkeypatch.setattr(document_processor, "extract_pdf_text_ocr", lambda _s: "")
    with pytest.raises(ValueError, match="pdf_text_missing"):
        document_processor.process_document_file(source, tmp_path / "out.jsonld")


def write_mojibake_pdf(path: Path) -> None:
    """Subset-font-shaped PDF: literal strings hold glyph indices, not text.

    Decoding these as Latin-1 yields accented mojibake — the real-world
    failure observed with word-processor exports. Synthetic T0 bytes only.
    """

    glyphs = bytes(range(0xC0, 0xFF)) * 4  # decodes to À..þ noise (<=400 chars per literal)
    body = b"BT (" + glyphs.replace(b"(", b" ").replace(b")", b" ") + b") Tj ET"
    path.write_bytes(
        b"%PDF-1.7\n1 0 obj <<>> stream\n" + body + b"\nendstream\nendobj\n%%EOF\n"
    )


def test_mojibake_pdf_never_reaches_reviewer(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Glyph-index literal strings must be refused, not shown as text."""

    source = tmp_path / "subsetfont.pdf"
    write_mojibake_pdf(source)
    monkeypatch.setattr(document_processor, "extract_pdf_text_pdftotext", lambda _s: "")
    monkeypatch.setattr(document_processor, "extract_pdf_text_pypdf", lambda _s: "")
    monkeypatch.setattr(document_processor, "extract_pdf_text_ocr", lambda _s: "")
    with pytest.raises(ValueError, match="pdf_text_unreadable"):
        document_processor.process_document_file(source, tmp_path / "out.jsonld")


def test_pdftotext_output_is_preferred_and_recorded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "report.pdf"
    write_mojibake_pdf(source)
    monkeypatch.setattr(
        document_processor,
        "extract_pdf_text_pdftotext",
        lambda _s: "Synthetic arrest report narrative for officer review.",
    )
    result = document_processor.process_document_file(source, tmp_path / "out.jsonld")
    assert result.extracted_fields["extraction_method"] == "pdftotext"
    assert "Synthetic arrest report narrative" in result.extracted_fields["extracted_text"]


def test_pypdf_fallback_is_used_and_recorded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "report.pdf"
    write_mojibake_pdf(source)
    monkeypatch.setattr(document_processor, "extract_pdf_text_pdftotext", lambda _s: "")
    monkeypatch.setattr(
        document_processor,
        "extract_pdf_text_pypdf",
        lambda _s: "Synthetic pypdf-extracted narrative for officer review.",
    )
    result = document_processor.process_document_file(source, tmp_path / "out.jsonld")
    assert result.extracted_fields["extraction_method"] == "pypdf"


def test_scanned_pdf_uses_ocr_fallback_when_available(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "scanned.pdf"
    write_scanned_pdf(source)
    monkeypatch.setattr(document_processor, "extract_pdf_text_pdftotext", lambda _s: "")
    monkeypatch.setattr(document_processor, "extract_pdf_text_pypdf", lambda _s: "")
    monkeypatch.setattr(
        document_processor,
        "extract_pdf_text_ocr",
        lambda _s: "Synthetic OCR text from scanned page.",
    )
    result = document_processor.process_document_file(source, tmp_path / "out.jsonld")
    assert result.extracted_fields["extraction_method"] == "ocr_tesseract"


def test_simple_literal_string_pdf_still_extracts_with_method(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """T0 generated PDFs with real ASCII literals keep working offline."""

    source = tmp_path / "invoice.pdf"
    write_pdf(source)
    monkeypatch.setattr(document_processor, "extract_pdf_text_pdftotext", lambda _s: "")
    monkeypatch.setattr(document_processor, "extract_pdf_text_pypdf", lambda _s: "")
    result = document_processor.process_document_file(source, tmp_path / "out.jsonld")
    assert result.extracted_fields["extraction_method"] == "literal_strings"
    assert "Synthetic PDF invoice" in result.extracted_fields["extracted_text"]


def test_text_looks_readable_gate() -> None:
    assert document_processor.text_looks_readable(
        "On 2026-01-15 the synthetic subject was arrested at 123 Demo Street."
    )
    assert not document_processor.text_looks_readable("¢ZÆÁ¿êéÆÅûþÂùuíEÜä¹îÄOÙøÚî¹ÉôÛb¹¦" * 4)
    assert not document_processor.text_looks_readable("   ")


def test_document_text_is_not_truncated_to_summary_bound(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Canonical reviewable text keeps full reports (bounded at MAX_DOCUMENT_TEXT)."""

    source = tmp_path / "long.pdf"
    write_mojibake_pdf(source)
    long_text = "Synthetic narrative sentence for review. " * 200  # ~8K chars
    monkeypatch.setattr(document_processor, "extract_pdf_text_pdftotext", lambda _s: long_text)
    result = document_processor.process_document_file(source, tmp_path / "out.jsonld")
    extracted_doc = json.loads(
        (tmp_path / "extracted-content.json").read_text(encoding="utf-8")
    )
    section_text = extracted_doc["content"]["sections"][0]["text"]
    assert len(section_text) > 5000
    assert result.extracted_fields["extracted_text"] == section_text[:240]


def test_xlsx_shared_strings_are_extracted(tmp_path: Path) -> None:
    source = tmp_path / "sheet.xlsx"
    write_xlsx(source)
    output = tmp_path / "sheet.jsonld"
    result = document_processor.process_document_file(source, output)
    assert "Synthetic spreadsheet cell Bravo" in result.extracted_fields["extracted_text"]


def test_office_without_text_fails_honestly(tmp_path: Path) -> None:
    source = tmp_path / "blank.docx"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types></Types>")
        archive.writestr("word/document.xml", "<w:document><w:body/></w:document>")
    with pytest.raises(ValueError, match="office_text_missing"):
        document_processor.process_document_file(source, tmp_path / "out.jsonld")


def test_image_without_embedded_text_fails_honestly_without_ocr(tmp_path: Path, monkeypatch) -> None:
    """No OCR engine: never emit placeholder 'Synthetic image file' content."""

    monkeypatch.setattr(document_processor.shutil, "which", lambda _name: None)
    source = tmp_path / "photo.jpg"
    source.write_bytes(b"\xff\xd8\xff\xe0synthetic-jpeg-bytes")
    with pytest.raises(ValueError, match="ocr_unavailable"):
        document_processor.process_document_file(source, tmp_path / "out.jsonld")


def test_no_placeholder_content_in_output(tmp_path: Path) -> None:
    source = tmp_path / "receipt.png"
    write_png_with_text(source, "Synthetic receipt total 12.34")
    output = tmp_path / "receipt.jsonld"
    document_processor.process_document_file(source, output)
    raw = output.read_text(encoding="utf-8")
    assert "Synthetic image file" not in raw


@pytest.mark.skipif(not document_processor.ocr_available(), reason="tesseract OCR CLI not installed")
def test_image_ocr_extracts_text_when_available(tmp_path: Path) -> None:
    """Live OCR path: a plain PNG goes through tesseract (may yield empty)."""

    source = tmp_path / "plain.png"
    write_plain_png(source)
    try:
        result = document_processor.process_document_file(source, tmp_path / "out.jsonld")
    except ValueError as exc:
        # A 1x1 image legitimately has no recognizable text.
        assert str(exc) == "no_extractable_content"
    else:
        assert result.extracted_fields["extraction_method"] == "ocr_tesseract"


def test_unsupported_kind_fails_honestly(tmp_path: Path) -> None:
    source = tmp_path / "binary.exe"
    source.write_bytes(b"MZ")
    with pytest.raises(ValueError, match="unsupported_file_kind"):
        document_processor.process_document_file(source, tmp_path / "out.jsonld")


@pytest.mark.parametrize(
    ("name", "payload", "file_kind"),
    [
        (
            "warrant.md",
            "# Search Warrant\n\nSubject Marcus Hale wallet 0xABC.\n",
            "markdown",
        ),
        (
            "chat.txt",
            "Operator: confirm transfer to synthetic wallet 0xABC\n",
            "plain_text",
        ),
        (
            "manifest.json",
            '{"case_slug":"fraud-crypto-synthetic-case","primary_victim":"Eleanor Vance"}',
            "json_metadata",
        ),
        (
            "flow.svg",
            '<svg><title>Flow</title><text x="1">Wallet 0xABC</text></svg>',
            "svg_image",
        ),
    ],
)
def test_warrant_return_kinds_produce_case_uco_graph(
    tmp_path: Path, name: str, payload: str, file_kind: str
) -> None:
    source = tmp_path / name
    source.write_text(payload, encoding="utf-8")
    output = tmp_path / f"{name}.jsonld"
    result = document_processor.process_document_file(
        source, output, file_kind=file_kind
    )
    assert result.file_kind == file_kind
    graph = json.loads(output.read_text(encoding="utf-8"))
    assert "@graph" in graph
    assert any(
        node.get("@type") == "case-investigation:InvestigativeAction"
        for node in graph["@graph"]
    )
    extracted, annotations = load_bundle(output)
    assert extracted["file_kind"] == file_kind
    assert annotations["@graph"]


def test_json_graph_upload_rejected_for_metadata_lane(tmp_path: Path) -> None:
    source = tmp_path / "graph.json"
    source.write_text('{"@context":{},"@graph":[]}', encoding="utf-8")
    with pytest.raises(ValueError, match="graph_import_required"):
        document_processor.process_document_file(source, tmp_path / "out.jsonld")


def test_oversized_source_fails_honestly(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(document_processor, "MAX_BYTES", 16)
    source = tmp_path / "table.csv"
    source.write_text("item,total\nalpha,12.34\n", encoding="utf-8")
    with pytest.raises(ValueError, match="source_oversized"):
        document_processor.process_document_file(source, tmp_path / "out.jsonld")


# ---------------------------------------------------------------------------
# Spec026 extraction bundle (contract 1.0): extracted-content.json + annotations.jsonld
# ---------------------------------------------------------------------------


def load_bundle(output: Path) -> tuple[dict, dict]:
    extracted = json.loads((output.parent / "extracted-content.json").read_text(encoding="utf-8"))
    annotations = json.loads((output.parent / "annotations.jsonld").read_text(encoding="utf-8"))
    return extracted, annotations


def assert_bundle_contract_shape(extracted: dict) -> None:
    assert extracted["contract_version"] == "1.0"
    assert extracted["extraction_tool"] == document_processor.TOOL_NAME
    assert extracted["extraction_tool_version"] == document_processor.TOOL_VERSION
    assert len(extracted["source_sha256"]) == 64
    assert len(extracted["content_sha256"]) == 64
    assert isinstance(extracted["failures"], list)


@pytest.mark.parametrize(
    ("writer", "name"),
    [
        (write_png_with_text, "receipt.png"),
        (write_pdf, "invoice.pdf"),
        (write_flate_pdf, "compressed.pdf"),
        (write_docx, "memo.docx"),
        (write_xlsx, "sheet.xlsx"),
    ],
)
def test_text_kinds_emit_anchored_bundle(tmp_path: Path, writer, name: str) -> None:
    source = tmp_path / name
    if writer is write_png_with_text:
        writer(source, "Synthetic receipt total 12.34")
    else:
        writer(source)
    output = tmp_path / "out.jsonld"
    result = document_processor.process_document_file(source, output)

    assert result.extracted_content_path is not None
    assert result.annotations_path is not None
    extracted, annotations = load_bundle(output)
    assert_bundle_contract_shape(extracted)

    # Text canonical model with a single section.
    assert extracted["content"]["kind"] == "text"
    sections = {s["section_id"]: s["text"] for s in extracted["content"]["sections"]}
    assert "s1" in sections

    # Every record is anchored; selector bounds are valid against the section.
    graph_record_ids = {
        node["@id"]
        for node in result.graph["@graph"]
        if node.get("@type")
        not in (
            "uco-tool:Tool",
            "case-investigation:InvestigativeAction",
            "uco-core:Relationship",
        )
        and not any(
            tag.startswith("link-look-file-kind:")
            for tag in (node.get("uco-core:tag") or [])
        )
    }
    annos = annotations["@graph"]
    assert len(annos) == len(result.records) >= 1
    for anno in annos:
        assert anno["body"] in graph_record_ids
        position = next(s for s in anno["target"]["selector"] if s["type"] == "TextPositionSelector")
        quote = next(s for s in anno["target"]["selector"] if s["type"] == "TextQuoteSelector")
        section_id = anno["target"]["source"].split("#", 1)[1]
        section_text = sections[section_id]
        assert 0 <= position["start"] < position["end"] <= len(section_text)
        assert section_text[position["start"] : position["end"]] == quote["exact"]


def test_csv_bundle_uses_rfc7111_row_selectors(tmp_path: Path) -> None:
    source = tmp_path / "table.csv"
    source.write_text("item,total\nalpha,12.34\nbravo,56.78\n", encoding="utf-8")
    output = tmp_path / "table.jsonld"
    document_processor.process_document_file(source, output)

    extracted, annotations = load_bundle(output)
    assert_bundle_contract_shape(extracted)
    sheet = extracted["content"]["sheets"][0]
    assert extracted["content"]["kind"] == "table"
    assert sheet["header"] == ["item", "total"]
    assert sheet["rows"] == [["alpha", "12.34"], ["bravo", "56.78"]]

    annos = annotations["@graph"]
    assert len(annos) == 2
    selectors = [a["target"]["selector"][0] for a in annos]
    assert all(s["type"] == "FragmentSelector" for s in selectors)
    assert all("rfc7111" in s["conformsTo"] for s in selectors)
    # Header is RFC 7111 row 1, so data rows are rows 2 and 3.
    assert [s["value"] for s in selectors] == ["row=2", "row=3"]
    # Row selectors stay within the canonical table bounds.
    for selector in selectors:
        row_number = int(selector["value"].split("=", 1)[1])
        assert 2 <= row_number <= len(sheet["rows"]) + 1


def test_duplicate_values_get_distinct_row_anchors(tmp_path: Path) -> None:
    """Two identical rows must anchor to distinct occurrences, never merged."""

    source = tmp_path / "dupes.csv"
    source.write_text("phone\n555-0100\n555-0100\n", encoding="utf-8")
    output = tmp_path / "dupes.jsonld"
    result = document_processor.process_document_file(source, output)

    _, annotations = load_bundle(output)
    annos = annotations["@graph"]
    assert len(annos) == len(result.records) == 2
    assert annos[0]["target"]["selector"][0]["value"] != annos[1]["target"]["selector"][0]["value"]
    assert annos[0]["body"] != annos[1]["body"]
    assert annos[0]["id"] != annos[1]["id"]


def test_annotations_reference_only_record_nodes(tmp_path: Path) -> None:
    """Honest absence: source/tool/action nodes are never annotated."""

    source = tmp_path / "receipt.png"
    write_png_with_text(source, "Synthetic receipt total 12.34")
    output = tmp_path / "receipt.jsonld"
    result = document_processor.process_document_file(source, output)

    _, annotations = load_bundle(output)
    non_record_ids = {
        node["@id"]
        for node in result.graph["@graph"]
        if node.get("@type")
        in ("uco-observable:RasterPicture", "uco-tool:Tool", "case-investigation:InvestigativeAction")
    }
    for anno in annotations["@graph"]:
        assert anno["body"] not in non_record_ids


def test_case_graph_vocabulary_unchanged_by_bundle(tmp_path: Path) -> None:
    """The bundle is additive: no annotation vocabulary leaks into the case graph."""

    source = tmp_path / "table.csv"
    source.write_text("item,total\nalpha,12.34\n", encoding="utf-8")
    output = tmp_path / "table.jsonld"
    document_processor.process_document_file(source, output)
    raw = output.read_text(encoding="utf-8")
    assert "TextPositionSelector" not in raw
    assert "oa:" not in raw
    assert "anno.jsonld" not in raw


def test_cli_reports_bundle_paths(tmp_path: Path, capsys) -> None:
    source = tmp_path / "table.csv"
    source.write_text("item,total\nalpha,12.34\n", encoding="utf-8")
    exit_code = document_processor.cli_main(
        ["--input", str(source), "--output", str(tmp_path / "out.jsonld")]
    )
    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["extracted_content_path"].endswith("extracted-content.json")
    assert payload["annotations_path"].endswith("annotations.jsonld")


# ---------------------------------------------------------------------------
# Progress contract (unchanged)
# ---------------------------------------------------------------------------


def test_process_document_file_emits_safe_progress_checkpoints(tmp_path: Path) -> None:
    source = tmp_path / "receipt.png"
    output = tmp_path / "receipt.jsonld"
    progress = tmp_path / "progress.jsonl"
    write_png_with_text(source, "Synthetic receipt total 12.34")

    document_processor.process_document_file(source, output, progress_output=progress)

    events = [
        json.loads(line)
        for line in progress.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    stages = [event["stage"] for event in events]
    assert stages == [
        "started",
        "inspect_source",
        "extract_content",
        "build_graph",
        "write_graph",
        "completed",
    ]
    assert events[-1]["percent"] == 100
    serialized = json.dumps(events)
    assert str(source) not in serialized
    assert "12.34" not in serialized
    assert "Synthetic receipt total" not in serialized


def test_process_document_file_emits_safe_failure_checkpoint(tmp_path: Path) -> None:
    progress = tmp_path / "progress.jsonl"
    missing_source = tmp_path / "missing.pdf"

    with pytest.raises(ValueError, match="source_missing"):
        document_processor.process_document_file(missing_source, tmp_path / "out.jsonld", progress_output=progress)

    events = [
        json.loads(line)
        for line in progress.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert events[-1]["stage"] == "failed"
    assert events[-1]["percent"] == 100
    assert str(missing_source) not in json.dumps(events)
