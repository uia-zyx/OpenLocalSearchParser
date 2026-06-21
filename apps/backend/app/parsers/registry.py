from app.domain.models import ProcessingStrategy
from app.parsers.base import ParsedDocument, StoredFile


class ParserRegistry:
    async def parse(self, file: StoredFile, strategy: ProcessingStrategy) -> ParsedDocument:
        if strategy == ProcessingStrategy.ocr_model:
            return self._placeholder_ocr_markdown(file, strategy)

        if strategy == ProcessingStrategy.scanner_ocr:
            return self._placeholder_ocr_markdown(file, strategy)

        return self._parse_text_like(file)

    def _parse_text_like(self, file: StoredFile) -> ParsedDocument:
        try:
            text = file.content.decode("utf-8")
        except UnicodeDecodeError:
            text = ""

        markdown = text if file.mime_type in {"text/markdown", "text/plain"} else self._stub_markdown(file)
        return ParsedDocument(
            title=file.filename,
            markdown=markdown,
            strategy=ProcessingStrategy.parser,
        )

    def _placeholder_ocr_markdown(
        self,
        file: StoredFile,
        strategy: ProcessingStrategy,
    ) -> ParsedDocument:
        return ParsedDocument(
            title=file.filename,
            markdown=self._stub_markdown(file),
            strategy=strategy,
            warnings=["OCR provider is not wired yet; placeholder Markdown was generated."],
        )

    def _stub_markdown(self, file: StoredFile) -> str:
        return (
            f"# {file.filename}\n\n"
            f"- MIME type: `{file.mime_type}`\n"
            "- Status: uploaded and ready for parser/OCR implementation.\n"
        )

