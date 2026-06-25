from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_search_service
from app.api.schemas import SearchRequest, SearchResponse
from app.search.service import SearchService

router = APIRouter(prefix="/mcp", tags=["mcp"])


@router.post(
    "/search",
    response_model=SearchResponse,
    operation_id="mcp_search_documents",
    summary="Search indexed documents from MCP clients",
    description=(
        "MCP-friendly search endpoint that uses the same embedding-first search pipeline "
        "as the public search API. This operation is also published as an MCP tool."
    ),
)
async def mcp_search_documents(
    request: SearchRequest,
    service: Annotated[SearchService, Depends(get_search_service)],
) -> SearchResponse:
    return SearchResponse(items=await service.search(request))
