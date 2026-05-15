import json
import struct
import sys
import zlib
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from document_processor import process_document_file


def write_png_with_text(path: Path, text: str) -> None:
    def chunk(kind: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(kind + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", crc)

    raw = b"\x00\xff\xff\xff"
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
        + chunk(b"tEXt", b"Receipt\x00Synthetic receipt total 12.34")
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


def write_pdf(path: Path) -> None:
    path.write_text(
        "%PDF-1.4\n1 0 obj <<>> stream\nBT (Synthetic PDF invoice total 23.45) Tj ET\nendstream\nendobj\n%%EOF\n",
        encoding="latin-1",
    )


def write_docx(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types></Types>")
        archive.writestr(
            "word/document.xml",
            "<w:document><w:body><w:t>Synthetic Office document item Alpha</w:t></w:body></w:document>",
        )


def test_process_live_acceptance_file_types(tmp_path: Path) -> None:
    fixtures = [
        ("receipt.png", lambda path: write_png_with_text(path, "Synthetic receipt total 12.34"), "receipt_image"),
        ("document.pdf", lambda path: write_pdf(path), "pdf"),
        ("document.docx", lambda path: write_docx(path), "office"),
        ("table.csv", lambda path: path.write_text("item,total\nalpha,12.34\n", encoding="utf-8"), "csv_table"),
    ]

    for name, writer, expected_kind in fixtures:
        source = tmp_path / name
        writer(source)
        output = tmp_path / f"{name}.jsonld"
        result = process_document_file(source, output)
        assert result.file_kind == expected_kind
        assert output.exists()
        doc = json.loads(output.read_text(encoding="utf-8"))
        graph = doc["@graph"]
        assert any(node.get("@type") == "case-investigation:InvestigativeAction" for node in graph)
        assert any(node.get("@type") == "uco-tool:Tool" for node in graph)
        assert any(node.get("@type") == "uco-core:UcoObject" for node in graph)
