from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.api.deps import get_document_repository, get_ingestion_service
from app.api.schemas import DocumentListItem, DocumentUploadResponse
from app.domain.models import ProcessingStrategy
from app.ingestion.service import IngestionService, InMemoryDocumentRepository

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentUploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_document(
    file: UploadFile = File(...),
    strategy: ProcessingStrategy = Form(...),
    service: IngestionService = Depends(get_ingestion_service),
) -> DocumentUploadResponse:
    content = await file.read()
    document, job_id = await service.ingest(
        filename=file.filename or "document",
        mime_type=file.content_type or "application/octet-stream",
        content=content,
        strategy=strategy,
    )

    return DocumentUploadResponse(document_id=document.id, job_id=job_id, status=document.status)


@router.get("", response_model=list[DocumentListItem])
async def list_documents(
    repository: InMemoryDocumentRepository = Depends(get_document_repository),
) -> list[DocumentListItem]:
    return [
        DocumentListItem(
            id=document.id,
            title=document.title,
            original_filename=document.original_filename,
            mime_type=document.mime_type,
            status=document.status,
            processing_strategy=document.processing_strategy,
        )
        for document in repository.list()
    ]


@router.get("/{document_id}/markdown", response_model=str)
async def get_document_markdown(
    document_id: UUID,
    repository: InMemoryDocumentRepository = Depends(get_document_repository),
) -> str:
    document = repository.get(document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    return document.markdown or ""

