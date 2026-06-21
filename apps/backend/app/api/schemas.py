from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.models import DocumentStatus, ProcessingStrategy, SearchResult


class DocumentUploadResponse(BaseModel):
    document_id: UUID
    job_id: UUID
    status: DocumentStatus


class DocumentListItem(BaseModel):
    id: UUID
    title: str
    original_filename: str
    mime_type: str
    status: DocumentStatus
    processing_strategy: ProcessingStrategy


class SearchFilters(BaseModel):
    mime_types: list[str] | None = None


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=10, ge=1, le=50)
    filters: SearchFilters | None = None


class SearchResponse(BaseModel):
    items: list[SearchResult]

