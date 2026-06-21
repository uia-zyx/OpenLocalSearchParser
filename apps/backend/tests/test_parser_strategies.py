import asyncio

from app.domain.models import ProcessingStrategy
from app.parsers.base import ParsedDocument, StoredFile
from app.parsers.registry import ParserRegistry


def test_scanner_ocr_pdf_uses_library_path(monkeypatch) -> None:
    registry = ParserRegistry()

    async def fail_model_ocr(
        file: StoredFile,
        strategy: ProcessingStrategy = ProcessingStrategy.ocr_model,
    ) -> ParsedDocument:
        raise AssertionError("scanner_ocr must not call model OCR")

    async def parse_pdf_with_libraries(file: StoredFile, strategy: ProcessingStrategy) -> ParsedDocument:
        return ParsedDocument(title=file.filename, markdown="# PDF", strategy=strategy)

    monkeypatch.setattr(registry, "_parse_with_ocr_model", fail_model_ocr)
    monkeypatch.setattr(registry, "_parse_pdf_with_libraries", parse_pdf_with_libraries)

    parsed = asyncio.run(
        registry.parse(
            StoredFile(filename="document.pdf", mime_type="application/pdf", content=b"%PDF"),
            ProcessingStrategy.scanner_ocr,
        )
    )

    assert parsed.strategy == ProcessingStrategy.scanner_ocr
    assert parsed.markdown == "# PDF"


def test_scanner_ocr_non_pdf_uses_library_path(monkeypatch) -> None:
    registry = ParserRegistry()

    async def fail_model_ocr(
        file: StoredFile,
        strategy: ProcessingStrategy = ProcessingStrategy.ocr_model,
    ) -> ParsedDocument:
        raise AssertionError("scanner_ocr must not call model OCR")

    async def parse_with_markitdown(file: StoredFile, strategy: ProcessingStrategy) -> ParsedDocument:
        return ParsedDocument(title=file.filename, markdown="# Text", strategy=strategy)

    monkeypatch.setattr(registry, "_parse_with_ocr_model", fail_model_ocr)
    monkeypatch.setattr(registry, "_parse_with_markitdown", parse_with_markitdown)

    parsed = asyncio.run(
        registry.parse(
            StoredFile(filename="document.txt", mime_type="text/plain", content=b"text"),
            ProcessingStrategy.scanner_ocr,
        )
    )

    assert parsed.strategy == ProcessingStrategy.scanner_ocr
    assert parsed.markdown == "# Text"
