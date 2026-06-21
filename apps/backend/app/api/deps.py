from functools import lru_cache

from app.ingestion.service import IngestionService, InMemoryDocumentRepository
from app.parsers.registry import ParserRegistry
from app.search.service import SearchService


@lru_cache
def get_document_repository() -> InMemoryDocumentRepository:
    return InMemoryDocumentRepository()


def get_ingestion_service() -> IngestionService:
    return IngestionService(
        repository=get_document_repository(),
        parser_registry=ParserRegistry(),
    )


def get_search_service() -> SearchService:
    return SearchService(repository=get_document_repository())

