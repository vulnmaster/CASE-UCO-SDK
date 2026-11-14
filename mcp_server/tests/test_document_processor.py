"""Tests for the canonical-term document processor (Tier T0 synthetic data)."""

import hashlib
import io
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
            "xl/workbook.xml",
            '<workbook xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheets><sheet name="Accounts" sheetId="1" r:id="rId1"/>'
            '<sheet name="Transactions" sheetId="2" r:id="rId2"/></sheets></workbook>',
        )
        archive.writestr(
            "xl/_rels/workbook.xml.rels",
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Target="worksheets/sheet1.xml"/>'
            '<Relationship Id="rId2" Target="worksheets/sheet2.xml"/>'
            "</Relationships>",
        )
        archive.writestr(
            "xl/sharedStrings.xml",
            '<sst><si><t>Synthetic spreadsheet cell Bravo</t></si>'
            '<si><t>Account</t></si><si><t>Amount</t></si></sst>',
        )
        archive.writestr(
            "xl/worksheets/sheet1.xml",
            '<worksheet><sheetData><row r="1"><c r="A1" t="s"><v>1</v></c>'
            '<c r="B1" t="s"><v>2</v></c></row><row r="2">'
            '<c r="A2" t="s"><v>0</v></c><c r="B2"><v>1250.50</v></c>'
            "</row></sheetData></worksheet>",
        )
        archive.writestr(
            "xl/worksheets/sheet2.xml",
            '<worksheet><sheetData><row r="1"><c r="A1" t="inlineStr">'
            '<is><t>Transaction ID</t></is></c><c r="B1" t="inlineStr">'
            '<is><t>Status</t></is></c></row><row r="2">'
            '<c r="A2" t="inlineStr"><is><t>tx-synthetic-1</t></is></c>'
            '<c r="B2" t="inlineStr"><is><t>complete</t></is></c>'
            "</row></sheetData></worksheet>",
        )


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
    document = json.loads(raw)
    declared = set(document["@context"])
    used = {
        key.split(":", 1)[0]
        for node in document["@graph"]
        for key in node
        if ":" in key and not key.startswith("@")
    }
    assert used <= declared, used - declared

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
    assert relationships[0]["uco-core:kindOfRelationship"] == "Extracted_From"
    record_ids = {n["@id"] for n in record_nodes}
    assert relationships[0]["uco-core:source"]["@id"] in record_ids


# ---------------------------------------------------------------------------
# Extraction breadth and honest failure (#103)
# ---------------------------------------------------------------------------


def test_csv_yields_bounded_per_record_candidates(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(document_processor, "MAX_CSV_RECORDS", 100)
    rows = "\n".join(f"row-{i},{i}.00" for i in range(1, 151))
    source = tmp_path / "big.csv"
    source.write_text("item,total\n" + rows + "\n", encoding="utf-8")
    output = tmp_path / "big.jsonld"
    result = document_processor.process_document_file(source, output)

    assert len(result.records) == 100
    assert result.truncated is True
    assert result.extracted_fields["truncated"].startswith("first 100")


def test_empty_csv_fails_honestly(tmp_path: Path) -> None:
    source = tmp_path / "empty.csv"
    source.write_text("item,total\n", encoding="utf-8")
    with pytest.raises(ValueError, match="empty_csv"):
        document_processor.process_document_file(source, tmp_path / "out.jsonld")


def test_binary_payload_with_csv_suffix_requires_preprocessing(tmp_path: Path) -> None:
    source = tmp_path / "decrypted_export.csv"
    source.write_bytes(
        b"\x1c\x1b<\\D\x17y6%(*-3[h)\x00\x02\x03"
        b"apparent,row\n"
        b"\x0e\x0fnot-actually-csv\x00\x1d"
    )

    with pytest.raises(ValueError, match="encrypted_or_binary_content"):
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


def test_confidentiality_stamp_is_sparse_page_text() -> None:
    assert document_processor.pdf_page_text_is_sparse("Adobe Proprietary and Confidential\n")
    assert document_processor.pdf_page_text_is_sparse("")
    assert not document_processor.pdf_page_text_is_sparse(
        "DECLARATION VERIFYING THE AUTHENTICITY OF CORPORATE RECORDS\n"
        "I certify that the attached records concern the registered user accounts "
        "named in the legal process and were kept in the regular course of business.\n"
    )


def test_mixed_pdf_ocrs_sparse_pages_and_keeps_typed_pages(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A typed cover page must not skip OCR on scanned warrant attachments."""

    source = tmp_path / "mixed.pdf"
    write_pdf(source)
    typed = (
        "DECLARATION VERIFYING THE AUTHENTICITY OF CORPORATE RECORDS\n"
        "I certify that the attached records concern the registered user accounts "
        "named in the legal process and were kept in the regular course of business.\n"
    )
    monkeypatch.setattr(document_processor, "extract_pdf_page_texts_pdftotext", lambda _s: [
        "Adobe Proprietary and Confidential\n",
        typed,
        "Adobe Proprietary and Confidential\n",
    ])
    monkeypatch.setattr(document_processor, "extract_pdf_page_texts_pypdf", lambda _s: [])
    monkeypatch.setattr(document_processor, "pdf_ocr_available", lambda: True)

    def fake_page_ocr(_source: Path, page_number: int) -> str:
        if page_number == 1:
            return "Attachment B of Affidavit for Search Warrant synthetic page one."
        if page_number == 3:
            return "Attachment B of Affidavit for Search Warrant synthetic page three."
        return ""

    monkeypatch.setattr(document_processor, "extract_pdf_page_ocr", fake_page_ocr)
    result = document_processor.process_document_file(source, tmp_path / "out.jsonld")
    text = json.loads((tmp_path / "extracted-content.json").read_text(encoding="utf-8"))
    section = text["content"]["sections"][0]["text"]
    assert result.extracted_fields["extraction_method"] == "pdftotext+ocr_tesseract"
    assert result.extracted_fields["pdf_ocr_pages"] == "2"
    assert result.extracted_fields["pdf_text_layer_pages"] == "1"
    assert "[PDF page 1]" in section
    assert "[PDF page 2]" in section
    assert "[PDF page 3]" in section
    assert "Affidavit for Search Warrant synthetic page one" in section
    assert "DECLARATION VERIFYING THE AUTHENTICITY" in section
    assert "Affidavit for Search Warrant synthetic page three" in section


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


def test_xlsx_preserves_sheets_numeric_cells_and_row_anchors(tmp_path: Path) -> None:
    source = tmp_path / "sheet.xlsx"
    write_xlsx(source)
    output = tmp_path / "sheet.jsonld"
    result = document_processor.process_document_file(source, output)

    assert "Synthetic spreadsheet cell Bravo" in result.extracted_fields["extracted_text"]
    assert result.extracted_fields["worksheet_count"] == "2"
    extracted = json.loads((tmp_path / "extracted-content.json").read_text(encoding="utf-8"))
    sheets = extracted["content"]["sheets"]
    assert [sheet["name"] for sheet in sheets] == ["Accounts", "Transactions"]
    assert sheets[0]["header"] == ["Account", "Amount"]
    assert sheets[0]["rows"][0] == ["Synthetic spreadsheet cell Bravo", "1250.50"]
    assert sheets[1]["rows"][0] == ["tx-synthetic-1", "complete"]
    assert result.records[0].anchor == {
        "selector_kind": "table_fragment",
        "sheet_name": "Accounts",
        "row_index": 1,
        "rfc7111_row": 2,
        "source_row_number": 2,
        "col_index": 0,
    }
    annotations = json.loads((tmp_path / "annotations.jsonld").read_text(encoding="utf-8"))
    assert annotations["@graph"][0]["target"]["source"].endswith("#Accounts")
    assert annotations["@graph"][0]["target"]["selector"][0]["value"] == "row=2;col=1"


def test_xlsx_worksheet_filter_emits_one_sheet(tmp_path: Path) -> None:
    source = tmp_path / "sheet.xlsx"
    write_xlsx(source)
    result = document_processor.process_document_file(
        source, tmp_path / "transactions.jsonld", worksheet="Transactions"
    )
    assert result.worksheet == "Transactions"
    texts = [record.text for record in result.records]
    assert any("tx-synthetic-1" in text for text in texts)
    assert not any("Synthetic spreadsheet cell Bravo" in text for text in texts)
    assert not (tmp_path / "extracted-content.json").exists()
    assert (tmp_path / "transactions.extracted-content.json").is_file()
    # The worksheet's annotations target the content file that was written.
    annotations = json.loads(result.annotations_path.read_text(encoding="utf-8"))
    sources = {item["target"]["source"].split("#")[0] for item in annotations["@graph"]}
    assert sources == {"transactions.extracted-content.json"}


def test_xlsx_partition_worksheets_writes_index_and_parts(tmp_path: Path) -> None:
    source = tmp_path / "sheet.xlsx"
    write_xlsx(source)
    output = tmp_path / "sheet.xlsx.jsonld"
    result = document_processor.process_document_file(
        source, output, partition_worksheets=True
    )
    assert result.extracted_fields["partition_count"] == "2"
    assert len(result.partition_outputs) == 2
    names = {path.name for path in result.partition_outputs}
    assert names == {"01-accounts.jsonld", "02-transactions.jsonld"}
    index_nodes = graph_nodes(output)
    assert any(
        node.get("@type") == "case-investigation:InvestigativeAction"
        and "worksheet graphs" in node.get("uco-core:name", "")
        for node in index_nodes
    )
    tools = nodes_of_type(index_nodes, "uco-tool:Tool")
    assert tools[0]["uco-tool:version"] == document_processor.TOOL_VERSION
    tx_graph = json.loads(
        (tmp_path / "sheet.xlsx.parts" / "02-transactions.jsonld").read_text(encoding="utf-8")
    )
    tx_text = json.dumps(tx_graph)
    assert "tx-synthetic-1" in tx_text
    assert "Synthetic spreadsheet cell Bravo" not in tx_text


def write_xlsx_five_rows(path: Path) -> None:
    rows_xml = ['<row r="1"><c r="A1" t="inlineStr"><is><t>Item</t></is></c></row>']
    for index in range(2, 7):
        rows_xml.append(
            f'<row r="{index}"><c r="A{index}" t="inlineStr">'
            f"<is><t>row-synthetic-{index}</t></is></c></row>"
        )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types></Types>")
        archive.writestr(
            "xl/workbook.xml",
            '<workbook xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheets><sheet name="Ledger" sheetId="1" r:id="rId1"/></sheets></workbook>',
        )
        archive.writestr(
            "xl/_rels/workbook.xml.rels",
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Target="worksheets/sheet1.xml"/>'
            "</Relationships>",
        )
        archive.writestr(
            "xl/worksheets/sheet1.xml",
            "<worksheet><sheetData>" + "".join(rows_xml) + "</sheetData></worksheet>",
        )


def test_xlsx_partition_windows_large_worksheets(tmp_path: Path) -> None:
    source = tmp_path / "ledger.xlsx"
    write_xlsx_five_rows(source)
    result = document_processor.process_document_file(
        source,
        tmp_path / "ledger.xlsx.jsonld",
        partition_worksheets=True,
        max_rows_per_graph=2,
    )
    assert len(result.partition_outputs) == 3
    names = [path.name for path in result.partition_outputs]
    assert names[0].startswith("01-ledger.r")
    first = json.dumps(json.loads(result.partition_outputs[0].read_text(encoding="utf-8")))
    last = json.dumps(json.loads(result.partition_outputs[-1].read_text(encoding="utf-8")))
    assert "row-synthetic-2" in first
    assert "row-synthetic-6" in last
    assert "row-synthetic-6" not in first


def test_html_message_export_is_reviewable_structured_text(tmp_path: Path) -> None:
    source = tmp_path / "return.html"
    source.write_text(
        "<html><body><h1>Synthetic provider return</h1><p>Account event Alpha</p></body></html>",
        encoding="utf-8",
    )
    result = document_processor.process_document_file(source, tmp_path / "out.jsonld")
    assert result.file_kind == "structured_text"
    assert result.extracted_fields["extraction_method"] == "html_parser"
    assert "Account event Alpha" in result.extracted_fields["extracted_text"]


def test_zip_archive_recurses_and_models_member_provenance(tmp_path: Path) -> None:
    nested = io.BytesIO()
    with zipfile.ZipFile(nested, "w") as archive:
        archive.writestr("inner/transactions.csv", "id,amount\ntx-1,25.00\n")
    source = tmp_path / "provider-return.zip"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("account/report.json", '{"account": "synthetic"}')
        archive.writestr("takeout.zip", nested.getvalue())

    result = document_processor.process_document_file(source, tmp_path / "out.jsonld")
    assert result.file_kind == "archive"
    assert result.extracted_fields["member_count"] == "3"
    assert result.extracted_fields["nested_archive_count"] == "1"
    assert any("transactions.csv" in record.label for record in result.records)
    extracted = json.loads((tmp_path / "extracted-content.json").read_text(encoding="utf-8"))
    combined = "\n".join(section["text"] for section in extracted["content"]["sections"])
    assert "tx-1,25.00" in combined


def test_zip_image_member_has_hashed_file_facets_and_extracted_from_relationship(
    tmp_path: Path,
) -> None:
    image = tmp_path / "profile.jpg"
    image.write_bytes(b"\xff\xd8\xffsynthetic-jpeg-evidence")
    digest = document_processor.hashlib.sha256(image.read_bytes()).hexdigest().upper()
    source = tmp_path / "provider-return.zip"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("images/profile.jpg", image.read_bytes())

    output = tmp_path / "out.jsonld"
    document_processor.process_document_file(source, output)
    nodes = graph_nodes(output)
    images = nodes_of_type(nodes, "uco-observable:RasterPicture")
    assert len(images) == 1
    facets = images[0]["uco-core:hasFacet"]
    file_facet = next(f for f in facets if f["@type"] == "uco-observable:FileFacet")
    content_facet = next(
        f for f in facets if f["@type"] == "uco-observable:ContentDataFacet"
    )
    assert file_facet["uco-observable:fileName"] == "profile.jpg"
    assert file_facet["uco-observable:extension"] == "jpg"
    assert content_facet["uco-observable:hash"][0]["uco-types:hashMethod"] == "SHA256"
    assert (
        content_facet["uco-observable:hash"][0]["uco-types:hashValue"]["@value"]
        == digest
    )

    source_node = next(
        node
        for node in nodes
        if node.get("@type") == "uco-observable:ObservableObject"
        and "source-file-kind:archive" in (node.get("uco-core:tag") or [])
    )
    relationship = next(
        node
        for node in nodes_of_type(nodes, "uco-core:Relationship")
        if node.get("uco-core:source", {}).get("@id") == images[0]["@id"]
    )
    assert relationship["uco-core:target"]["@id"] == source_node["@id"]
    assert relationship["uco-core:kindOfRelationship"] == "Extracted_From"
    assert relationship["uco-core:isDirectional"] is True


def test_zip_archive_accepts_valid_content_without_zip_suffix(tmp_path: Path) -> None:
    source = tmp_path / "bounded-upload-name"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("account/report.txt", "synthetic account record")

    assert document_processor.normalize_file_kind("archive", source) == "archive"
    result = document_processor.process_document_file(
        source, tmp_path / "out.jsonld", file_kind="archive"
    )

    assert result.file_kind == "archive"
    assert result.extracted_fields["member_count"] == "1"


def test_zip_archive_refuses_path_traversal(tmp_path: Path) -> None:
    source = tmp_path / "unsafe.zip"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("../escape.txt", "synthetic")
    with pytest.raises(ValueError, match="archive_unsafe_path"):
        document_processor.process_document_file(source, tmp_path / "out.jsonld")


def test_new_warrant_return_extensions_route_to_supported_kinds(tmp_path: Path) -> None:
    expected = {
        "return.xls": "legacy_office",
        "mailbox.mbox": "structured_text",
        "message.msg": "structured_text",
        "events.ics": "structured_text",
        "contacts.vcf": "structured_text",
        "bundle.zip": "archive",
    }
    for name, kind in expected.items():
        assert document_processor.normalize_file_kind(None, tmp_path / name) == kind


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
    """Live OCR path preserves a plain image even when no text is found."""

    source = tmp_path / "plain.png"
    write_plain_png(source)
    try:
        result = document_processor.process_document_file(source, tmp_path / "out.jsonld")
    except ValueError as exc:
        # Some installed Tesseract/image-library combinations reject a 1x1
        # image before recognition; that remains an honest OCR failure.
        assert str(exc) == "ocr_failed"
    else:
        assert result.extracted_fields["extraction_method"] in {
            "ocr_tesseract",
            "image_metadata_only",
        }
        if result.extracted_fields["extraction_method"] == "image_metadata_only":
            assert result.extracted_fields["ocr_status"] == "no_text_detected"
            assert result.records == []
            assert result.extracted_content_path is None


def test_image_with_empty_ocr_is_preserved_as_metadata_only(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(document_processor, "ocr_available", lambda: True)
    monkeypatch.setattr(document_processor, "run_ocr", lambda _source: "")
    source = tmp_path / "photo.jpg"
    source.write_bytes(b"\xff\xd8\xff\xe0synthetic-jpeg-bytes")

    result = document_processor.process_document_file(source, tmp_path / "out.jsonld")

    assert result.file_kind == "receipt_image"
    assert result.extracted_fields["extraction_method"] == "image_metadata_only"
    assert result.extracted_fields["ocr_status"] == "no_text_detected"
    assert result.records == []
    assert result.extracted_content_path is None
    source_nodes = [
        node
        for node in result.graph["@graph"]
        if node.get("@type") == "uco-observable:RasterPicture"
    ]
    assert len(source_nodes) == 1
    assert "Synthetic image file" not in json.dumps(result.graph)


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
            tag.startswith("source-file-kind:")
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


def test_duplicate_values_share_entity_but_keep_distinct_row_anchors(tmp_path: Path) -> None:
    """Repeated identifiers are one graph identity with every occurrence anchored."""

    source = tmp_path / "dupes.csv"
    source.write_text("phone\n202-555-0100\n202-555-0100\n", encoding="utf-8")
    output = tmp_path / "dupes.jsonld"
    result = document_processor.process_document_file(source, output)

    _, annotations = load_bundle(output)
    annos = annotations["@graph"]
    assert len(result.records) == 1
    assert len(annos) == 2
    assert annos[0]["target"]["selector"][0]["value"] != annos[1]["target"]["selector"][0]["value"]
    assert annos[0]["body"] == annos[1]["body"]
    assert annos[0]["id"] != annos[1]["id"]


def test_distinct_structured_values_never_share_a_uco_facet(tmp_path: Path) -> None:
    """Cell-local semantic offsets must not collapse distinct entity facets."""

    source = tmp_path / "accounts.csv"
    source.write_text(
        "email,ip\n"
        "first@example.test,192.0.2.10\n"
        "second@example.test,192.0.2.11\n",
        encoding="utf-8",
    )
    result = document_processor.process_document_file(source, tmp_path / "out.jsonld")
    entities = [
        node
        for node in result.graph["@graph"]
        if node.get("@type") in {
            "uco-observable:EmailAddress",
            "uco-observable:IPAddress",
        }
    ]
    facet_ids = [facet["@id"] for node in entities for facet in node["uco-core:hasFacet"]]
    assert len(entities) == 4
    assert len(facet_ids) == len(set(facet_ids))


def test_provider_rows_preserve_timestamped_cross_dataset_context(tmp_path: Path) -> None:
    """Account-control clues remain linked in a source-row Event."""

    source = tmp_path / "access-log.csv"
    bitcoin = "bc1q" + "q" * 38
    source.write_text(
        "timestamp,email,ip,adid,city,country,wallet_address\n"
        f"2025-07-09 04:14:00,analyst@example.test,129.224.203.200,"
        f"00000000-0000-4000-8000-000000000001,Hong Kong,HK,{bitcoin}\n",
        encoding="utf-8",
    )
    result = document_processor.process_document_file(source, tmp_path / "out.jsonld")
    graph = result.graph["@graph"]

    event = next(node for node in graph if node.get("@type") == "uco-core:Event")
    assert event["uco-core:startTime"][0]["@value"] == "2025-07-09T04:14:00"
    context_ids = {ref["@id"] for ref in event["uco-core:eventContext"]}
    context_nodes = [node for node in graph if node.get("@id") in context_ids]
    assert {
        "uco-observable:EmailAddress",
        "uco-observable:IPAddress",
        "uco-observable:Device",
        "uco-location:Location",
        "uco-observable:ObservableObject",
    }.issubset({node.get("@type") for node in context_nodes})
    dictionary = event["uco-core:eventAttribute"][0]
    assert {entry["uco-types:key"] for entry in dictionary["uco-types:entry"]} == {
        "timestamp", "email", "ip", "adid", "city", "country", "wallet_address"
    }
    address = next(
        node
        for node in context_nodes
        if node.get("@type") == "uco-observable:ObservableObject"
        and any(
            facet.get("@type") == "cryptoinv:CryptocurrencyAddressFacet"
            for facet in node.get("uco-core:hasFacet", [])
        )
    )
    address_facet = next(
        facet
        for facet in address["uco-core:hasFacet"]
        if facet["@type"] == "cryptoinv:CryptocurrencyAddressFacet"
    )
    assert address_facet["cryptoinv:addressValue"] == bitcoin
    assert address_facet["cryptoinv:cryptocurrencyType"] == "BTC"
    provenance = next(
        node for node in graph if node.get("@type") == "case-investigation:ProvenanceRecord"
    )
    rooted_ids = {ref["@id"] for ref in provenance["uco-core:object"]}
    assert event["@id"] in rooted_ids
    assert any(node.get("@type") == "case-investigation:InvestigativeAction" and node["@id"] in rooted_ids for node in graph)


def test_vasp_ledger_rows_use_cryptoinv_facets(tmp_path: Path) -> None:
    """Provider deposit rows keep ledger IDs distinct from on-chain hashes."""

    bitcoin = "bc1q" + "q" * 38
    onchain = "ab" * 32
    source = tmp_path / "Report_BNB-108014_deposit.csv"
    source.write_text(
        "Date(UTC),Coin,Network,Amount,TransactionFee,Address,TxID,Status,Deposit ID,Wallet\n"
        f"2024-01-15 12:00:00,BTC,BTC,0.5,0.0001,{bitcoin},{onchain},Completed,DEP-001,Spot\n"
        "2024-01-16 13:00:00,USDT,TRC20,100,0,,,Successful,DEP-002,Funding\n",
        encoding="utf-8",
    )
    result = document_processor.process_document_file(source, tmp_path / "out.jsonld")
    graph = result.graph["@graph"]
    assert result.graph["@context"]["cryptoinv"] == "http://example.org/ontology/cryptoinv/"

    vasp = next(
        node for node in graph if node.get("@type") == "cryptoinv:VirtualAssetServiceProvider"
    )
    assert vasp["uco-core:name"] == "Binance"

    events = [node for node in graph if node.get("@type") == "uco-core:Event"]
    assert len(events) == 2
    onchain_event = next(
        event
        for event in events
        if any(
            facet.get("@type") == "cryptoinv:CryptocurrencyTransactionFacet"
            for facet in event.get("uco-core:hasFacet", [])
        )
    )
    ledger = next(
        facet
        for facet in onchain_event["uco-core:hasFacet"]
        if facet["@type"] == "cryptoinv:VirtualAssetLedgerRecordFacet"
    )
    assert ledger["cryptoinv:ledgerRecordType"] == "Deposit"
    assert ledger["cryptoinv:providerTransactionId"] == "DEP-001"
    assert ledger["cryptoinv:isOnChain"] is True
    assert ledger["cryptoinv:assetSymbol"] == "BTC"
    tx = next(
        facet
        for facet in onchain_event["uco-core:hasFacet"]
        if facet["@type"] == "cryptoinv:CryptocurrencyTransactionFacet"
    )
    assert tx["cryptoinv:transactionHash"] == onchain
    assert tx["cryptoinv:transactionType"] == "Deposit"
    assert {"@id": vasp["@id"]} in onchain_event["uco-core:eventContext"]

    internal = next(event for event in events if event is not onchain_event)
    internal_ledger = next(
        facet
        for facet in internal["uco-core:hasFacet"]
        if facet["@type"] == "cryptoinv:VirtualAssetLedgerRecordFacet"
    )
    assert internal_ledger["cryptoinv:isOnChain"] is False
    assert internal_ledger["cryptoinv:providerTransactionId"] == "DEP-002"
    assert not any(
        facet.get("@type") == "cryptoinv:CryptocurrencyTransactionFacet"
        for facet in internal.get("uco-core:hasFacet", [])
    )

    compartments = {
        facet["cryptoinv:hostedWalletCompartment"]
        for node in graph
        for facet in node.get("uco-core:hasFacet", [])
        if facet.get("@type") == "cryptoinv:CryptocurrencyWalletFacet"
    }
    assert compartments == {"Spot", "Funding"}


def test_advertising_ids_normalize_for_cross_return_join(tmp_path: Path) -> None:
    """GAID/AdID values are stored case-folded so later SPARQL joins match."""

    adid = "AA000000-0000-4000-8000-000000000001"
    source = tmp_path / "devices.csv"
    source.write_text(
        "timestamp,gaid,ip\n"
        f"2025-07-09 04:14:00,{adid},203.0.113.10\n"
        f"2025-07-09 04:15:00,{adid.lower()},203.0.113.11\n",
        encoding="utf-8",
    )
    result = document_processor.process_document_file(source, tmp_path / "out.jsonld")
    devices = [
        node
        for node in result.graph["@graph"]
        if node.get("@type") == "uco-observable:Device"
    ]
    assert len(devices) == 1
    facet = next(
        item
        for item in devices[0]["uco-core:hasFacet"]
        if item.get("@type") == "uco-observable:OperatingSystemFacet"
    )
    assert facet["uco-observable:advertisingID"] == [adid.casefold()]


def test_vasp_hint_uses_parent_folder_when_filename_is_opaque(tmp_path: Path) -> None:
    folder = tmp_path / "OKX Return"
    folder.mkdir()
    source = folder / "UUID-615125427199583129.csv"
    source.write_text("item,total\nalpha,1\n", encoding="utf-8")
    result = document_processor.process_document_file(source, tmp_path / "out.jsonld")
    vasp = next(
        node
        for node in result.graph["@graph"]
        if node.get("@type") == "cryptoinv:VirtualAssetServiceProvider"
    )
    assert vasp["uco-core:name"] == "OKX"


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


def test_two_documents_in_one_directory_keep_their_own_bundles(tmp_path: Path) -> None:
    """Issue #92: the returned sidecar paths must still describe their own
    document after a second document is processed into the same directory."""
    out_dir = tmp_path / "out"
    first_source = tmp_path / "a.txt"
    second_source = tmp_path / "b.txt"
    first_source.write_text(
        "Memo one. The laptop was seized on 2024-01-15 by Agent Smith.\n", encoding="utf-8"
    )
    second_source.write_text(
        "Memo two. The phone was imaged on 2024-02-20 by Agent Jones.\n", encoding="utf-8"
    )
    first = document_processor.process_document_file(
        first_source, out_dir / "a.jsonld", file_kind="plain_text"
    )
    second = document_processor.process_document_file(
        second_source, out_dir / "b.jsonld", file_kind="plain_text"
    )

    assert first.extracted_content_path == out_dir / "a.extracted-content.json"
    assert first.annotations_path == out_dir / "a.annotations.jsonld"
    assert second.extracted_content_path == out_dir / "b.extracted-content.json"
    assert second.annotations_path == out_dir / "b.annotations.jsonld"

    for result in (first, second):
        assert result.extracted_content_path is not None
        assert result.annotations_path is not None
        extracted = json.loads(result.extracted_content_path.read_text(encoding="utf-8"))
        assert extracted["source_sha256"] == result.sha256
        annotations = json.loads(result.annotations_path.read_text(encoding="utf-8"))
        sources = {item["target"]["source"].split("#")[0] for item in annotations["@graph"]}
        assert sources == {result.extracted_content_path.name}
    assert first.sha256 != second.sha256

    # The shared names remain for single-document directories and describe
    # the document processed last.
    shared = json.loads((out_dir / "extracted-content.json").read_text(encoding="utf-8"))
    assert shared["source_sha256"] == second.sha256


def test_cli_reports_bundle_paths(tmp_path: Path, capsys) -> None:
    source = tmp_path / "table.csv"
    source.write_text("item,total\nalpha,12.34\n", encoding="utf-8")
    exit_code = document_processor.cli_main(
        ["--input", str(source), "--output", str(tmp_path / "out.jsonld")]
    )
    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["extracted_content_path"] == str(tmp_path / "out.extracted-content.json")
    assert payload["annotations_path"] == str(tmp_path / "out.annotations.jsonld")


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


def _synthetic_p2pkh() -> str:
    from document_semantic_mapping import _B58_ALPHABET

    body = b"\x00" + bytes(range(20))
    checksum = hashlib.sha256(hashlib.sha256(body).digest()).digest()[:4]
    data = body + checksum
    number = int.from_bytes(data, "big")
    chars: list[str] = []
    while number:
        number, remainder = divmod(number, 58)
        chars.append(_B58_ALPHABET[remainder])
    pad = 0
    for byte in data:
        if byte == 0:
            pad += 1
        else:
            break
    return ("1" * pad) + "".join(reversed(chars))


def test_plain_text_warrant_emits_investigation_and_typed_address(
    tmp_path: Path,
) -> None:
    address = _synthetic_p2pkh()
    broken = " ".join(address[i : i + 4] for i in range(0, len(address), 4))
    source = tmp_path / "warrant.txt"
    source.write_text(
        "ATTACHMENT A OF AFFIDAVIT\n"
        "This search warrant concerns a cryptocurrency investment scam using "
        f"Binance and wallet-portal.cc. Destination {broken}.\n",
        encoding="utf-8",
    )
    output = tmp_path / "warrant.jsonld"
    document_processor.process_document_file(source, output)
    nodes = graph_nodes(output)
    investigations = nodes_of_type(nodes, "case-investigation:Investigation")
    assert len(investigations) == 1
    assert investigations[0].get("uco-core:object")
    assert investigations[0].get("case-investigation:relevantAuthorization")
    assert nodes_of_type(nodes, "case-investigation:Authorization")
    assert nodes_of_type(nodes, "cryptoinv:VirtualAssetServiceProvider")
    address_values = [
        facet.get("cryptoinv:addressValue")
        for node in nodes
        for facet in node.get("uco-core:hasFacet") or []
        if facet.get("@type") == "cryptoinv:CryptocurrencyAddressFacet"
    ]
    assert address in address_values
    string_values = [
        item.get("uco-observable:stringValue", "")
        for node in nodes
        for facet in node.get("uco-core:hasFacet") or []
        for item in facet.get("uco-observable:strings") or []
    ]
    assert any(address in value for value in string_values)
    assert not any(broken in value for value in string_values)


def _capture(tmp_path: Path, **capture) -> list[dict]:
    source = tmp_path / "order.csv"
    source.write_text("item,total\nalpha,12.34\n", encoding="utf-8")
    output = tmp_path / "order.jsonld"
    document_processor.process_document_file(source, output, **capture)
    return graph_nodes(output)


def test_capture_provenance_records_url_and_retrieval(tmp_path: Path) -> None:
    nodes = _capture(
        tmp_path,
        source_url="https://records.example.org/orders/1.csv",
        retrieved_at="2026-10-07T22:32:51Z",
        http_status=200,
    )
    [url] = nodes_of_type(nodes, "uco-observable:URL")
    assert url["uco-core:hasFacet"][0]["uco-observable:fullValue"] == (
        "https://records.example.org/orders/1.csv"
    )
    [retrieval] = [
        n for n in nodes_of_type(nodes, "case-investigation:InvestigativeAction")
        if n.get("uco-action:object") == {"@id": url["@id"]}
    ]
    [source] = [n for n in nodes if "source-file-kind:" in str(n.get("uco-core:tag"))]
    assert retrieval["uco-action:result"] == {"@id": source["@id"]}
    assert retrieval["uco-action:endTime"] == {
        "@type": "xsd:dateTime", "@value": "2026-10-07T22:32:51+00:00",
    }
    [status] = retrieval["uco-core:hasFacet"]
    assert (status["uco-action:argumentName"], status["uco-action:value"]) == ("http_status", "200")

    from case_uco.validation.graph import validate_graph_file, validator_available

    if validator_available():
        report = validate_graph_file(tmp_path / "order.jsonld")
        assert report.conforms is True, report.safe_summary


def test_capture_date_only_writes_no_end_time(tmp_path: Path) -> None:
    nodes = _capture(
        tmp_path, source_url="https://records.example.org/orders/1.csv", retrieved_at="2026-10-07"
    )
    [retrieval] = [n for n in nodes if str(n.get("uco-core:name", "")).startswith("Retrieval of")]
    assert "uco-action:endTime" not in retrieval
    assert "2026-10-07" in retrieval["uco-core:description"]


def test_no_capture_provenance_leaves_graph_unchanged(tmp_path: Path) -> None:
    nodes = _capture(tmp_path)
    assert not nodes_of_type(nodes, "uco-observable:URL")
    assert not [n for n in nodes if str(n.get("uco-core:name", "")).startswith("Retrieval of")]


@pytest.mark.parametrize(
    ("capture", "error"),
    [
        ({"source_url": "file:///etc/passwd"}, "source_url_invalid"),
        ({"source_url": "https://user:secret@records.example.org/x"}, "source_url_invalid"),
        ({"source_url": "https://records.example.org/a b"}, "source_url_invalid"),
        ({"source_url": "records.example.org/x"}, "source_url_invalid"),
        ({"source_url": "https://records.example.org/x", "retrieved_at": "yesterday"}, "retrieved_at_invalid"),
        ({"source_url": "https://records.example.org/x", "http_status": 99}, "http_status_invalid"),
        ({"retrieved_at": "2026-10-07"}, "capture_requires_source_url"),
    ],
)
def test_capture_provenance_rejects_bad_values(tmp_path: Path, capture: dict, error: str) -> None:
    with pytest.raises(ValueError, match=error):
        _capture(tmp_path, **capture)
