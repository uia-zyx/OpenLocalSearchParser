from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.api.deps import get_search_service
from app.api.schemas import SearchRequest, SearchResponse
from app.search.service import SearchService

router = APIRouter(prefix="/mcp", tags=["mcp"])
compat_router = APIRouter(prefix="/mcp", tags=["mcp"])


@router.get("/search/openapi.json", include_in_schema=False)
async def mcp_search_openapi(http_request: Request) -> dict[str, object]:
    server_url = str(http_request.url).removesuffix("/openapi.json").rstrip("/")
    return _search_tool_openapi(server_url=server_url, search_path="/")


@compat_router.get("/openapi.json", include_in_schema=False)
async def mcp_protocol_search_openapi(http_request: Request) -> dict[str, object]:
    server_url = str(http_request.url).removesuffix("/openapi.json").rstrip("/")
    return _search_tool_openapi(server_url=server_url, search_path="/search")


def _search_tool_openapi(server_url: str, search_path: str) -> dict[str, object]:
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "OpenLocalSearchParser Search Tool",
            "version": "0.1.0",
            "description": "OpenAPI tool server for searching indexed local documents.",
        },
        "servers": [{"url": server_url}],
        "paths": {
            search_path: {
                "post": {
                    "operationId": "mcp_search_documents",
                    "summary": "Search indexed local documents",
                    "description": "Search recognized and indexed documents by query.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SearchRequest"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Search results",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/SearchResponse"}
                                }
                            },
                        },
                        "422": {"description": "Validation error"},
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "SearchRequest": SearchRequest.model_json_schema(
                    ref_template="#/components/schemas/{model}"
                ),
                "SearchResponse": SearchResponse.model_json_schema(
                    ref_template="#/components/schemas/{model}"
                ),
            }
        },
    }


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


@router.post("/search/", response_model=SearchResponse, include_in_schema=False)
async def mcp_search_documents_with_trailing_slash(
    request: SearchRequest,
    service: Annotated[SearchService, Depends(get_search_service)],
) -> SearchResponse:
    return await mcp_search_documents(request, service)


@compat_router.post("/search", response_model=SearchResponse, include_in_schema=False)
async def mcp_protocol_search_documents(
    request: SearchRequest,
    service: Annotated[SearchService, Depends(get_search_service)],
) -> SearchResponse:
    return await mcp_search_documents(request, service)


@compat_router.post("/search/", response_model=SearchResponse, include_in_schema=False)
async def mcp_protocol_search_documents_with_trailing_slash(
    request: SearchRequest,
    service: Annotated[SearchService, Depends(get_search_service)],
) -> SearchResponse:
    return await mcp_search_documents(request, service)
