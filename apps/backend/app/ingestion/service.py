import hashlib
from uuid import UUID, uuid4

from app.domain.models import Document, DocumentStatus, ProcessingStrategy
from app.parsers.base import StoredFile
from app.parsers.registry import ParserRegistry
from app.search.chunking import chunk_markdown


class InMemoryDocumentRepository:
    def __init__(self) -> None:
        self.documents: dict[UUID, Document] = {}

    def save(self, document: Document) -> Document:
        self.documents[document.id] = document
        return document

    def list(self) -> list[Document]:
        return sorted(self.documents.values(), key=lambda item: item.created_at, reverse=True)

    def get(self, document_id: UUID) -> Document | None:
        return self.documents.get(document_id)

    def find_by_content_hash(self, content_hash: str) -> Document | None:
        return next(
            (document for document in self.documents.values() if document.content_hash == content_hash),
            None,
        )

    def delete(self, document_id: UUID) -> bool:
        return self.documents.pop(document_id, None) is not None


class IngestionService:
    def __init__(
        self,
        repository: InMemoryDocumentRepository,
        parser_registry: ParserRegistry,
    ) -> None:
        self.repository = repository
        self.parser_registry = parser_registry

    async def ingest(
        self,
        filename: str,
        mime_type: str,
        content: bytes,
        strategy: ProcessingStrategy,
    ) -> tuple[Document, UUID, bool]:
        content_hash = hashlib.sha256(content).hexdigest()
        existing_document = self.repository.find_by_content_hash(content_hash)
        if existing_document is not None:
            return existing_document, uuid4(), True

        file = StoredFile(filename=filename, mime_type=mime_type, content=content)
        parsed = await self.parser_registry.parse(file, strategy)

        document = Document(
            title=parsed.title,
            original_filename=filename,
            mime_type=mime_type,
            original_content=content,
            content_hash=content_hash,
            status=DocumentStatus.indexed,
            processing_strategy=parsed.strategy,
            markdown=parsed.markdown,
        )
        self.repository.save(document)

        # The chunking call is intentionally kept here so API contracts already match ingestion.
        chunk_markdown(document.id, parsed.markdown)
        return document, uuid4(), False

