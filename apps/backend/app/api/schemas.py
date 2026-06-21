from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.models import DocumentStatus, ProcessingStrategy, SearchResult


class DocumentUploadResponse(BaseModel):
    document_id: UUID
    job_id: UUID
    status: DocumentStatus
    deduplicated: bool = False


class DocumentListItem(BaseModel):
    id: UUID
    title: str
    original_filename: str
    mime_type: str
    status: DocumentStatus
    processing_strategy: ProcessingStrategy


class DocumentUpdateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class SearchFilters(BaseModel):
    mime_types: list[str] | None = None


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=10, ge=1, le=50)
    filters: SearchFilters | None = None


class SearchResponse(BaseModel):
    items: list[SearchResult]


class OpenWebUISearchRequest(BaseModel):
    query: str = Field(min_length=1)
    count: int = Field(default=5, ge=1, le=50)


class OpenWebUISearchResult(BaseModel):
    link: str
    title: str
    snippet: str


class OpenWebUILoaderRequest(BaseModel):
    urls: list[str] = Field(min_length=1, max_length=20)


class OpenWebUILoaderResult(BaseModel):
    page_content: str
    metadata: dict[str, str]

